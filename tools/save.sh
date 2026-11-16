#!/bin/bash
git config user.name "github-actions"
git config user.email "actions@github.com"
git add -A
git commit -m "$1" || true
git pull --rebase -q || true
git push || true
