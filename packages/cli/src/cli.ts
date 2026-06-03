#!/usr/bin/env node
import { Command } from 'commander';

const program = new Command();

program
  .name('sea')
  .description('Shattered Sea wiki CLI')
  .version('0.1.0');

program.parse();
