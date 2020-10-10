#!/bin/bash
kill -9 `ps -aux|grep uwsgi3|grep -v "grep"|awk '{ print $2 }'`
