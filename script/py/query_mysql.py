#!/usr/bin/env python3
"""
MySQL 数据库操作工具
支持：SQL 查询、DDL/DML 执行、HTTP 请求
"""

import argparse
import json
import sys
from typing import Optional, Dict, Any, List

try:
    import pymysql
    from pymysql.cursors import DictCursor
except ImportError:
    print("错误: 缺少 pymysql 库")
    print("请运行: pip install pymysql")
    sys.exit(1)

try:
    import requests
except ImportError:
    requests = None


class MySQLClient:
    def __init__(self, host: str, port: int, user: str, password: str, database: str, charset: str = 'utf8mb4'):
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
            'charset': charset,
            'cursorclass': DictCursor
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(**self.config)
            return True
        except Exception as e:
            print(json.dumps({'error': f'连接失败: {str(e)}', 'success': False}, ensure_ascii=False))
            return False

    def close(self):
        if self.connection:
            self.connection.close()

    def query(self, sql: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        if not self.connect():
            return {'success': False}
        
        try:
            with self.connection.cursor() as cursor:  # type: ignore
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return {
                    'success': True,
                    'data': rows,
                    'rowcount': len(rows),
                    'fields': [desc[0] for desc in cursor.description] if cursor.description else []
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            self.close()

    def execute(self, sql: str, params: Optional[tuple] = None) -> Dict[str, Any]:
        if not self.connect():
            return {'success': False}
        
        try:
            with self.connection.cursor() as cursor:  # type: ignore
                affected = cursor.execute(sql, params)
                self.connection.commit()  # type: ignore
                return {
                    'success': True,
                    'affected_rows': affected,
                    'lastrowid': cursor.lastrowid
                }
        except Exception as e:
            self.connection.rollback()  # type: ignore
            return {'success': False, 'error': str(e)}
        finally:
            self.close()

    def execute_many(self, sql: str, params_list: List[tuple]) -> Dict[str, Any]:
        if not self.connect():
            return {'success': False}
        
        try:
            with self.connection.cursor() as cursor:  # type: ignore
                affected = cursor.executemany(sql, params_list)
                self.connection.commit()  # type: ignore
                return {
                    'success': True,
                    'affected_rows': affected
                }
        except Exception as e:
            self.connection.rollback()  # type: ignore
            return {'success': False, 'error': str(e)}
        finally:
            self.close()

    def show_tables(self) -> Dict[str, Any]:
        return self.query("SHOW TABLES")

    def describe_table(self, table: str) -> Dict[str, Any]:
        return self.query(f"DESCRIBE `{table}`")

    def show_create_table(self, table: str) -> Dict[str, Any]:
        return self.query(f"SHOW CREATE TABLE `{table}`")


def format_output(data: Dict[str, Any], format_type: str = 'json') -> str:
    if format_type == 'json':
        return json.dumps(data, ensure_ascii=False, indent=2)
    elif format_type == 'table' and 'data' in data:
        if not data['data']:
            return "无数据"
        
        fields = data.get('fields', [])
        rows = data['data']
        
        col_widths = {}
        for field in fields:
            col_widths[field] = len(field)
            for row in rows:
                val_len = len(str(row.get(field, '')))
                if val_len > col_widths[field]:
                    col_widths[field] = min(val_len, 50)
        
        header = ' | '.join(f.ljust(col_widths[f]) for f in fields)
        separator = '-+-'.join('-' * col_widths[f] for f in fields)
        
        lines = [header, separator]
        for row in rows:
            line = ' | '.join(str(row.get(f, ''))[:col_widths[f]].ljust(col_widths[f]) for f in fields)
            lines.append(line)
        
        return '\n'.join(lines)
    else:
        return json.dumps(data, ensure_ascii=False, indent=2)


def curl_request(method: str, url: str, headers: Optional[Dict] = None, 
                 data: Optional[Dict] = None, json_data: Optional[Dict] = None,
                 params: Optional[Dict] = None, timeout: int = 30) -> Dict[str, Any]:
    if requests is None:
        return {'success': False, 'error': '缺少 requests 库，请运行: pip install requests'}
    
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers or {},
            data=data,
            json=json_data,
            params=params,
            timeout=timeout
        )
        
        result = {
            'success': True,
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'url': response.url
        }
        
        try:
            result['json'] = response.json()
        except:
            result['text'] = response.text
        
        return result
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    parser = argparse.ArgumentParser(description='MySQL 数据库操作工具')
    
    parser.add_argument('--host', default='localhost', help='数据库主机')
    parser.add_argument('--port', type=int, default=3306, help='数据库端口')
    parser.add_argument('--user', required=False, help='数据库用户名')
    parser.add_argument('--password', required=False, help='数据库密码')
    parser.add_argument('--database', required=False, help='数据库名称')
    parser.add_argument('--format', choices=['json', 'table'], default='json', help='输出格式')
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    query_parser = subparsers.add_parser('query', help='执行 SELECT 查询')
    query_parser.add_argument('sql', help='SQL 查询语句')
    
    exec_parser = subparsers.add_parser('execute', help='执行 INSERT/UPDATE/DELETE/DDL')
    exec_parser.add_argument('sql', help='SQL 语句')
    
    tables_parser = subparsers.add_parser('tables', help='显示所有表')
    
    desc_parser = subparsers.add_parser('describe', help='显示表结构')
    desc_parser.add_argument('table', help='表名')
    
    create_parser = subparsers.add_parser('show-create', help='显示建表语句')
    create_parser.add_argument('table', help='表名')
    
    curl_parser = subparsers.add_parser('curl', help='执行 HTTP 请求')
    curl_parser.add_argument('url', help='请求 URL')
    curl_parser.add_argument('-X', '--method', default='GET', help='HTTP 方法')
    curl_parser.add_argument('-H', '--header', action='append', help='请求头 (格式: Key: Value)')
    curl_parser.add_argument('-d', '--data', help='请求体数据')
    curl_parser.add_argument('--json', help='JSON 请求体')
    curl_parser.add_argument('--timeout', type=int, default=30, help='超时时间（秒）')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'curl':
        headers = {}
        if args.header:
            for h in args.header:
                if ':' in h:
                    k, v = h.split(':', 1)
                    headers[k.strip()] = v.strip()
        
        json_data = None
        data = None
        if args.json:
            try:
                json_data = json.loads(args.json)
            except:
                data = args.json
        elif args.data:
            data = args.data
        
        result = curl_request(
            method=args.method,
            url=args.url,
            headers=headers,
            data=data,
            json_data=json_data,
            timeout=args.timeout
        )
        print(format_output(result, 'json'))
        sys.exit(0 if result.get('success') else 1)
    
    if not all([args.user, args.password, args.database]):
        print("错误: 数据库操作需要 --user, --password, --database 参数")
        sys.exit(1)
    
    client = MySQLClient(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database
    )
    
    result: Dict[str, Any] = {'success': False, 'error': 'Unknown command'}
    
    if args.command == 'query':
        result = client.query(args.sql)
        print(format_output(result, args.format))
    elif args.command == 'execute':
        result = client.execute(args.sql)
        print(format_output(result, args.format))
    elif args.command == 'tables':
        result = client.show_tables()
        print(format_output(result, args.format))
    elif args.command == 'describe':
        result = client.describe_table(args.table)
        print(format_output(result, args.format))
    elif args.command == 'show-create':
        result = client.show_create_table(args.table)
        print(format_output(result, args.format))
    
    sys.exit(0 if result.get('success', True) else 1)


if __name__ == '__main__':
    main()
