#!/bin/bash
git add .
git commit -m "photo pull"
git push
ssh thomas@zen-hacking.com "cd /var/www/photo-blog && git pull"
