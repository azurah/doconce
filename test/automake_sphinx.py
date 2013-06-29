#!/usr/bin/env python
# Autogenerated file (by doconce sphinx_dir)
# Purpose: create HTML Sphinx version of admon

# Command-line arguments are transferred to the doconce format sphinx file
# compilation command

import glob, sys, os, commands, shutil

command_line_options = ' '.join(['"%s"' % arg for arg in sys.argv[1:]])

sphinx_rootdir = 'tmp_admon'

def system(cmd, capture_output=False, echo=True):
    if echo:
        print 'running', cmd
    if capture_output:
        failure, outtext = commands.getstatusoutput(cmd) # Unix/Linux only
    else:
        failure = os.system(cmd)
    if failure:
        print 'Could not run', cmd
        sys.exit(1)
    if capture_output:
        return outtext

filename = 'admon'
if not os.path.isfile(filename + '.rst'):
    # Filter doconce format to sphinx format and copy to sphinx directory
    cmd = 'doconce format sphinx %s %s' % (filename, command_line_options)
    print cmd
    system(cmd)

    # Fix: utf-8 encoding for non-English chars
    cmd = 'doconce guess_encoding %s.rst' % filename
    enc = system(cmd, capture_output=True)
    if enc == "iso-8859-1":
        # sphinx does not like non-English characters in iso-8859-1
        system('doconce change_encoding iso-8859-1 utf-8 %s.rst' % filename)

# Copy generated sphinx file to sphinx root directory
shutil.copy('%s.rst' % filename, sphinx_rootdir)

# Copy figures and movies directories
figdirs = glob.glob('fig*') + glob.glob('mov*')
for figdir in figdirs:
    destdir = os.path.join(sphinx_rootdir, figdir)
    if os.path.isdir(figdir) and not os.path.isdir(destdir):
        print 'copying', figdir, 'to', sphinx_rootdir
        shutil.copytree(figdir, destdir)

# Copy needed media files in current dir (not in fig* and mov*)
for rstfile in [os.path.join(sphinx_rootdir, filename + '.rst')]:
    f = open(rstfile, 'r')
    text = text_orig = f.read()
    f.close()
    import re
    media_files = [name.strip() for name in
                   re.findall('.. figure:: (.+)', text)]
    local_media_files = [name for name in media_files if not os.sep in name]

    for name in media_files:
        basename = os.path.basename(name)
        if name.startswith('http') or name.startswith('ftp'):
            pass
        else:
            if not os.path.isfile(os.path.join(sphinx_rootdir, basename)):
                print 'copying', name, 'to', sphinx_rootdir
                shutil.copy(name, sphinx_rootdir)
            if name not in local_media_files:
                # name lies in another directory, make local reference to it
                # since it is copied to sphinx_rootdir
                text = text.replace('.. figure:: %s' % name,
                                    '.. figure:: %s' % basename)
    if text != text_orig:
        f = open(rstfile, 'w')
        f.write(text)
        f.close()

# Copy linked local files, placed in _static*, to tmp_admon/_static
staticdirs = glob.glob('_static*')
for staticdir in staticdirs:
    system('cp -r %s/* tmp_admon/_static/' % staticdir)
    # (Note: must do cp -r since shutil.copy/copytree cannot copy a la cp -r)

# Compile web version of the sphinx document
os.chdir(sphinx_rootdir)
print os.getcwd()
system('make clean')
system('make html')

print 'Fix generated files:'
os.chdir('_build/html')
for filename in glob.glob('*.html'):
    # Fix double title in <title> tags
    system('doconce subst "<title>(.+?) &mdash;.+?</title>" "<title>\g<1></title>" %s' % filename, echo=False)
    # Fix admonition style
    system("""doconce replace "</head>" "
   <style type="text/css">
     div.admonition {
       background-color: whiteSmoke;
       border: 1px solid #bababa;
     }
   </style>
  </head>
" %s""" % filename, echo=False)
    os.remove(filename + '.old~')
print """
google-chrome tmp_admon/_build/html/index.html
"""
