Documentation
=============


Write docstrings according to the [Google python style guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html#Comments).

```
sphinx-apidoc -e --dry-run -o docs niprov
```
*Update auto-doc sources*

```
cd docs
make html
```
*Re-build html output*
