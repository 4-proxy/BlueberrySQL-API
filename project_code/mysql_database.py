# -*- coding: utf-8 -*-

"""
description

Copyright 2024 4-proxy
Apache license, version 2.0 (Apache-2.0 license)
"""

__all__: list[str] = [
    "MySQLDataBase",
]

__author__ = "4-proxy"
__version__ = "0.8.1"

from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection

from settings_dto import PoolConfigDTO

from typing import Any, Dict


# ______________________________________________________________________________________________________________________
class MySQLDataBase:
    def __init__(self, pool_config: PoolConfigDTO, **dbconfig: Any) -> None:
        self._set_pool_config(pool_config=pool_config)
        self._dbconfig: Dict[str, Any] = dbconfig
        self._pool: MySQLConnectionPool = self.create_connection_pool()

    # ------------------------------------------------------------------------------------------------------------------
    def _set_pool_config(self, pool_config: PoolConfigDTO) -> None:
        if not isinstance(pool_config, PoolConfigDTO):
            raise AttributeError(
                f"pool_config must be an instance of `PoolConfigDTO`! Obtained instance: {type(pool_config)}"
            )
        self._pool_config: PoolConfigDTO = pool_config

    # ------------------------------------------------------------------------------------------------------------------
    def create_connection_pool(self) -> MySQLConnectionPool:
        name: str = self._pool_config.pool_name
        size: int = self._pool_config.pool_size
        reset_session: bool = self._pool_config.pool_reset_session

        pool = MySQLConnectionPool(
            pool_name=name,
            pool_size=size,
            pool_reset_session=reset_session,
            **self._dbconfig
        )

        return pool

    # ------------------------------------------------------------------------------------------------------------------
    def change_dbconfig_for_connection_pool(self, new_dbconfig: Dict[str, Any]) -> None:
        self._pool.set_config(**new_dbconfig)

    # ------------------------------------------------------------------------------------------------------------------
    def get_connection_from_pool(self) -> PooledMySQLConnection:
        connection: PooledMySQLConnection = self._pool.get_connection()

        return connection

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        from string import Template
        from textwrap import dedent

        raw_template = Template(
            """
            MySQL server Info:
                Version: $server_version
                Host: $server_host
                Port: $server_port
                Time Zone: $server_time_zone

            Connection Info:
                User: $connection_user
                Database: $connection_database

            Pool Info:
                Name: $pool_name
                Size: $pool_size
                Reset Session: $pool_reset_session
            """
        )

        server_info: Dict[str, str] = self._get_info_about_server()
        connection_info: Dict[str, str] = self._get_info_about_connection()
        pool_info: Dict[str, str] = self._get_info_about_pool()

        fill_template: str = raw_template.safe_substitute(
            **server_info,
            **connection_info,
            **pool_info
        )

        final_template: str = dedent(text=fill_template)

        return final_template

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_server(self) -> Dict[str, str]:
        with self.get_connection_from_pool() as connection:
            version: str = connection.get_server_info()
            host: str = connection.server_host
            port: int = connection.server_port
            time_zone: str = connection.time_zone

            server_info: Dict[str, str] = {
                "server_version": version,
                "server_host": host,
                "server_port": str(port),
                "server_time_zone": time_zone,
            }

        return server_info

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_connection(self) -> Dict[str, str]:
        with self.get_connection_from_pool() as connection:
            user: str = connection.user
            database_name: str = connection.database

            connection_info: Dict[str, str] = {
                "connection_user": user,
                "connection_database": database_name,
            }

        return connection_info

    # ------------------------------------------------------------------------------------------------------------------
    def _get_info_about_pool(self) -> Dict[str, str]:
        pool: MySQLConnectionPool = self._pool

        pool_info: Dict[str, str] = {
            "pool_name": pool.pool_name,
            "pool_size": str(pool.pool_size),
            "pool_reset_session": str(pool.reset_session),
        }

        return pool_info
