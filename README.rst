==========
auto_py2to3
==========

On January 1, 2020, the Python 2 code base was frozen. From that day on, there was no further porting of Python 2, which actually made the language and runtime environment obsolete.
Core developer Nick Coghlan explained in the FAQ, which ended "the core development team maintained Python 2 and 3 as reference interpreters for about 13 years."
The final version of Python 2 is currently in the beta testing and release candidate phase, and the final production version python 2.7.18 is expected to be released in April 2020.
Although most people in the Python community believe that Python needs urgent changes-especially since the much-needed Unicode support already exists.
But many people are frustrated that Python 2 code works well. Therefore, code migration is needed, and the ultimate goal of the library is to realize automated and fast code migration and provide automated testing.
In this process, although there may be some unsatisfactory aspects in the code migration process, the library will continue to be iterated and maintained.

Architecture
------------

* Relying on the official 2to3 as a technical tool, encapsulating executable files for later use.
* Provide multiple functions through the command line to process project code.

Version Support
------------
* 2.x  to 3.x

Development Planning
------------

1. Single file 2to3, run test cases. (Finished test)
2. Single file 2to3, relying on library version retrieval and analysis, and running test cases. (Finished test)
3. Single file 2to3, relying on library version upgrade and corresponding function upgrade, running test cases. (Finished test)
4. Simple project structure transfer all py files as a whole, and run test cases. (Finished test)
5. Test the conversion effects of several mainstream libraries, and modify optimization bugs. (Developing)

Usage Example
------------
.. image:: /example/ticketGrabbingExample-test processing.png

Contribution Get Started!
------------

Ready to contribute or user? Here's how to set up `auto_py2to3` for local development.

1. Fork the `auto_py2to3` repo on Gitee.
2. Clone your fork locally::

    $ git clone https://gitee.com/weihaitong/auto_py2to3.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv auto_py2to3
    $ cd auto_py2to3/
    $ pipenv install -r requirements_dev.txt

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Commit your changes and push your branch to Gitee::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the Gitee website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.rst.
3. The pull request should work for Python 3.x.
   and make sure that the tests pass for all supported Python versions.
