#!/bin/bash
kill -9 `ps -aux|grep uwsgi|grep -v "grep"|awk '{ print $2 }'`
