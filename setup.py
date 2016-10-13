from setuptools import setup

setup(
      	name="AntAIML",
      	version="1.1",
      	author="qingpei.gqp",
      	author_email="qingpei.gqp@alipay.com",
	    license="LGPL",
	    description="An interpreter package for AIML, the Artificial Intelligence Markup Language",
    	long_description="""PyAIML implements an interpreter for AIML, the Artificial Intelligence
Markup Language developed by Dr. Richard Wallace of the A.L.I.C.E. Foundation.
It can be used to implement a conversational AI program.""",
	    platforms=["any"],
	    packages= ['aiml'],
		classifiers=["Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Intended Audience :: Developers",
                 "Programming Language :: Python",
                 "Operating System :: OS Independent",
                 "Topic :: Communications :: Chat",
                 "Topic :: Scientific/Engineering :: Artificial Intelligence"
                 ],
      )
