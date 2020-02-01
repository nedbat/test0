# Makefile for Getting Started Testing

SAMPLES = \
	portfolio1.py portfolio2.py portfolio3.py \
	porttest1.py porttest2.py porttest3.py porttest3_broken.py \
	test_port1_unittest.py test_port2_unittest.py test_port2_unittest_broken.py \
	test_port3_unittest.py test_port3_unittest_broken.py test_port3_unittest_broken2.py \
	test_port3b_unittest.py \
	test_port4_unittest.py test_port4_unittest_broken.py test_port5_unittest.py \
	test_port6_unittest.py test_port7_unittest.py test_port8_unittest.py test_port9_unittest.py \
	test_port1_pytest.py \
	test_port2_pytest.py test_port2_pytest_broken.py \
	test_port3_pytest_broken2.py \
	test_port4_pytest.py test_port4_pytest_broken.py \
	test_port5_pytest.py \
	test_port6_pytest.py

PY_OUT = porttest1.out porttest2.out porttest3.out porttest3_broken.out

UNIT_OUT = \
	test_port1_unittest.out \
	test_port2_unittest.out test_port2_unittest_broken.out \
	test_port3_unittest.out test_port3_unittest_broken.out test_port3_unittest_broken2.out \
	test_port4_unittest.out test_port4_unittest_broken.out \
	test_port5_unittest.out \
	test_port6_unittest.out \
	test_port9_unittest.out

PYTEST_OUT = \
	test_port1_pytest.out \
	test_port2_pytest.out test_port2_pytest_broken.out \
	test_port3_pytest_broken2.out \
	test_port4_pytest.out test_port4_pytest_broken.out \
	test_port5_pytest.out \
	test_port6_pytest.out

COVERAGE_UNIT_OUT = test_port7_unittest.out test_port8_unittest.out

COVERAGE_PYTEST_OUT = test_port7_pytest.out

OUTPUT = $(PY_OUT) $(UNIT_OUT) $(COVERAGE_UNIT_OUT) $(PYTEST_OUT) $(COVERAGE_PYTEST_OUT)

SLUG = test0

SLIDE_HTML = $(SLUG).html
SAMPLE_ZIP = $(SLUG).zip

EXTRA_HTML = extra.html

IMAGES = \
	img/dadtoon-chaos-2.png img/dadtoon-iambad-3.png img/dadtoon-mii.png \
	img/happysticks.png img/mock.png \
	img/github.png img/twitter.png
SD = slippy
JS_FILES = \
	$(SD)/jquery.min.js $(SD)/jquery.history.js $(SD)/slippy.js \
	slides.js lineselect.js typogr.min.js
CSS_FILES = \
	$(SD)/slippy.css $(SD)/slippy-pure.css \
	slides.css
SLIDE_SUPPORT = $(JS_FILES) $(CSS_FILES) $(IMAGES)

.PHONY: $(SLIDE_HTML) $(EXTRA_HTML)

slides: $(SLIDE_HTML) $(EXTRA_HTML)

$(SLIDE_HTML): $(SAMPLES) $(OUTPUT)
	python -m cogapp -r $@

$(EXTRA_HTML): $(SAMPLES) $(OUTPUT)
	python -m cogapp -r $@

$(PY_OUT): *.py portfolio1.py portfolio2.py portfolio3.py
	@echo "$$ python $*.py" > $@
	-python $*.py >> $@ 2>&1

$(UNIT_OUT): *.py
	@echo "$$ python -m unittest $*" > $@
	-python -m unittest $* >> $@ 2>&1

$(COVERAGE_UNIT_OUT): test_port7_unittest.py test_port8_unittest.py portfolio3.py
	@echo "$$ coverage run -m unittest $*" > $@
	coverage run -m unittest $* >> $@ 2>&1
	@echo "$$ coverage report -m" >> $@
	coverage report -m >> $@

$(PYTEST_OUT): *.py
	@echo "$$ pytest -q $*.py" > $@
	-COLUMNS=68 pytest -q $*.py >> $@ 2>&1

$(COVERAGE_PYTEST_OUT): test_port7_pytest.py portfolio3.py
	@echo "$$ coverage run -m pytest -q $*.py" > $@
	coverage run --include=portfolio3.py,$*.py -m pytest -q $*.py >> $@ 2>&1
	@echo "$$ coverage report -m" >> $@
	coverage report -m >> $@

develop: slides
	watchmedo shell-command -W -c "make slides"

clean:
	rm -f $(OUTPUT)
	rm -f $(SAMPLE_ZIP) $(PX)
	rm -f *.pyc
	rm -rf __pycache__
	rm -f .coverage
	rm -rf $(PNG_DIR)

zip $(SAMPLE_ZIP): $(SAMPLES)
	zip $(SAMPLE_ZIP) $(SAMPLES)

tar $(TARFILE): $(SLIDE_HTML) $(SAMPLES) $(SLIDE_SUPPORT) Makefile
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
