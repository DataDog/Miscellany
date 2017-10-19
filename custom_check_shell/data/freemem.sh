#!/bin/bash
# NOTE: This does not work -- and isn't used by this custom check -- it's here for posterity sake; See the README.
free | grep Mem | awk '{print $3/$2 * 100.0}'
