#!/bin/bash
echo ssh $(hostname) $@
ssh $(hostname) $@
