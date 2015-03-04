#!/usr/bin/env python
"""Run all example programs in this directory. Report execution failures."""


import glob, os, sys, commands, shutil
programs = sorted(glob.glob('*.py'))
remove = ['runtests.py',
          'u_layered.py',  # just an autogenerated file
          'vcp2D.py', # hangs in os.system - of unknown reason 
          ]
for filename in remove:
    programs.remove(filename)
# make sure define_layers.py is run prior to Poisson_layers.py:
programs.insert(0, 'define_layers.py')
print 'Testing', programs

# Copy programs to separate folder and modify the codes such that
# plotting is inactive
tempdir = 'tmp0'
if os.path.isdir(tempdir):
   shutil.rmtree(tempdir)
os.mkdir(tempdir)
for program in programs:
    shutil.copy(program, tempdir)
os.chdir(tempdir)
cmd = "scitools subst 'from dolfin import \*' 'from dolfin import *\nfrom scitools.misc import DoNothing\nplot = DoNothing()' *.py"
os.system(cmd)
cmd = """scitools subst "raw_input\('Press Return: '\)" "" *.py"""
os.system(cmd)

command_line_arguments = {
    'std': '1 10 10',
    'sin_daD.py': '1 1.5 30 4',
    'dn2_paD.py': '1 1 10 10',
    }

failures = []
for program in programs:
    print '\n\n\nRunning', program
    if program in command_line_arguments:
        cml = command_line_arguments[program]
    else:
        cml = command_line_arguments['std']  # dummy choice
    failure, output = commands.getstatusoutput('python ' + program + ' ' + cml)
    print output
    if failure:
        failures.append((program, output))

for item in failures:
    print '\nProgram %s failed with\n%s' % (item[0], item[1])
for item in failures:
    print '\nProgram %s failed' % (item[0])



    
