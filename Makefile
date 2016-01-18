# Makefile for Getting Started Testing

SAMPLES = \
	portfolio1.py portfolio2.py portfolio3.py \
	porttest1.py porttest2.py porttest3.py porttest3_broken.py \
	test_port1.py test_port2.py test_port2_broken.py \
	test_port3.py test_port3_broken.py test_port3_broken2.py \
	test_port3b.py \
	test_port4.py test_port4_broken.py test_port5.py \
	test_port6.py test_port7.py test_port8.py test_port9.py

PY_OUT = porttest1.out porttest2.out porttest3.out porttest3_broken.out

UNIT_OUT = \
	test_port1.out test_port2.out test_port2_broken.out \
	test_port3.out test_port3_broken.out test_port3_broken2.out \
	test_port4.out test_port4_broken.out \
	test_port5.out test_port6.out test_port9.out

PYTEST_OUT = \
	test_port1_pytest.out test_port2_pytest.out test_port2_pytest_broken.out \
	test_port3_pytest_broken2.out \
	test_port6_pytest.out

COVERAGE_OUT = test_port7.out test_port8.out

OUTPUT = $(PY_OUT) $(UNIT_OUT) $(COVERAGE_OUT) $(PYTEST_OUT)

SLUG = test0

SLIDE_HTML = $(SLUG).html
SAMPLE_ZIP = $(SLUG).zip

IMAGES = dadtoon-chaos-2.png dadtoon-iambad-3.png dadtoon-mii.png happysticks.png mock.png
SD = slippy/src
JS_FILES = $(SD)/jquery.min.js $(SD)/jquery.history.js $(SD)/slippy.js lineselect.js
CSS_FILES = $(SD)/slippy.css $(SD)/slippy-pure.css
SLIDE_SUPPORT = $(JS_FILES) $(CSS_FILES) $(IMAGES)

.PHONY: $(SLIDE_HTML)

slides: $(SLIDE_HTML)

$(SLIDE_HTML): $(SAMPLES) $(OUTPUT)
	python cog.py -r $@

$(PY_OUT): *.py portfolio1.py portfolio2.py portfolio3.py
	echo "$$ python $*.py" > $@
	-python $*.py >> $@ 2>&1

$(UNIT_OUT): *.py
	echo "$$ python -m unittest $*" > $@
	-python -m unittest $* >> $@ 2>&1

$(COVERAGE_OUT): test_port7.py test_port8.py portfolio3.py
	echo "$$ coverage run -m unittest $*" > $@
	coverage run -m unittest $* >> $@ 2>&1
	echo "$$ coverage report -m" >> $@
	coverage report -m >> $@

$(PYTEST_OUT): *.py
	echo "$$ py.test -q $*.py" > $@
	-py.test -q $*.py >> $@ 2>&1

clean:
	rm -f $(OUTPUT)
	rm -f $(SAMPLE_ZIP) $(PX)
	rm -f *.pyc
	rm -rf __pycache__
	rm -f .coverage
	rm -rf $(PNG_DIR)

zip $(SAMPLE_ZIP): $(SAMPLES)
	zip $(SAMPLE_ZIP) $(SAMPLES)

tar $(TARFILE): $(SLIDE_HTML) $(SAMPLES) $(SLIDE_SUPPORT) Makefile cog.py
	tar czvf $(TARFILE) --mode=777 $^

PNG_DIR = png

pngs: $(SLIDE_HTML)
	phantomjs phantom-slippy-to-png.js $(SLIDE_HTML) $(PNG_DIR)/ $(SLUG)_

WEBHOME = ~/web/stellated/pages/text
WEBPRZHOME = $(WEBHOME)/$(SLUG)

PX = $(SLUG).px

px $(PX): $(SLIDE_HTML)
	python slippy_to_px.py $(SLIDE_HTML) $(PX) $(SLUG)

publish: $(SLIDE_HTML) $(SAMPLE_ZIP) $(PX) pngs
	cp -f $(PX) $(WEBHOME)
	rm -rf $(WEBPRZHOME)
	mkdir -p $(WEBPRZHOME)/slippy/src
	cp $(PNG_DIR)/*.png $(IMAGES) $(WEBPRZHOME)
	echo $(SLIDE_SUPPORT) | xargs -n1 -I{} cp {} $(WEBPRZHOME)/{}
	cp -f $(SLIDE_HTML) $(WEBPRZHOME)
	cp -f $(SAMPLE_ZIP) $(WEBPRZHOME)
