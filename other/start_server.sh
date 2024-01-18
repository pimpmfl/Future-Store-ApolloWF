#!/bin/bash
echo "Starting redis server with JSON module.."
cd redis-stable
redis-server ./redis.conf --loadmodule /home/ubuntu/RedisJSON/target/release/librejson.so