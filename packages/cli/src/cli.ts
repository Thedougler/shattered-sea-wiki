#!/usr/bin/env node
import { Command } from 'commander';
import { fixCommand } from './commands/fix.js';
import { indexCommand } from './commands/index-regen.js';
import { taxonomyCommand } from './commands/taxonomy.js';

const program = new Command();

program.name('sea').description('Shattered Sea wiki CLI').version('0.1.0');

program.addCommand(fixCommand);
program.addCommand(indexCommand);
program.addCommand(taxonomyCommand);

program.parse();
