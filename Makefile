# Makefile for Getting Started Testing

SAMPLES = \
	portfolio1.py portfolio2.py portfolio3.py \
	porttest1.py porttest2.py porttest3.py porttest3_broken.py \
	test_port1.py test_port2.py test_port2_broken.py test_port3.py test_port3_broken.py test_port3_broken2.py \
	test_port4.py test_port4_broken.py test_port5.py test_port6.py test_port7.py test_port8.py test_port9.py

OUTPUT = \
	porttest1.out porttest2.out porttest3.out porttest3_broken.out \
	test_port1.out test_port2.out test_port2_broken.out test_port3.out test_port3_broken.out test_port3_broken2.out \
	test_port4.out test_port4_broken.out \
	test_port7.out test_port8.out

SLIDE_HTML = test0.html
SAMPLE_ZIP = test0.zip

IMAGES = dodeca3_500.png
SD = slippy/src
JS_FILES = $(SD)/jquery-1.4.2.min.js $(SD)/jquery.history.js $(SD)/slippy-0.9.0.js 
CSS_FILES = $(SD)/slippy-0.9.0.css neds.css
SLIDE_SUPPORT = $(JS_FILES) $(CSS_FILES) $(IMAGES)

.PHONY: $(SLIDE_HTML)

slides: $(SLIDE_HTML)

$(SLIDE_HTML): $(SAMPLES) $(OUTPUT)
	python cog.py -r $@

%.out : %.py portfolio1.py portfolio2.py portfolio3.py
	echo "$$ python $*.py" > $@
	-python $*.py >> $@ 2>&1

test_port7.out test_port8.out : test_port7.py test_port8.py portfolio3.py
	echo "$$ coverage run $*.py" > $@
	coverage run $*.py >> $@ 2>&1
	echo "$$ coverage report -m" >> $@
	coverage report -m >> $@

clean:
	rm -f $(OUTPUT)
	rm -f $(SAMPLE_ZIP)
	rm -f *.pyc
	rm -rf __pycache__
	rm -f .coverage

zip $(SAMPLE_ZIP): $(SAMPLES)
	zip $(SAMPLE_ZIP) $(SAMPLES)

tar $(TARFILE): $(SLIDE_HTML) $(SAMPLES) $(SLIDE_SUPPORT) Makefile cog.py
	tar czvf $(TARFILE) --mode=777 $^

WEBHOME = c:/ned/web/stellated/pages/text

publish: $(SLIDE_HTML) $(SAMPLE_ZIP)
	cp $(SLIDE_HTML) $(WEBHOME)/st.html
	svn export --force starttest_stuff $(WEBHOME)/starttest_stuff
	cp $(SAMPLE_ZIP) $(WEBHOME)
