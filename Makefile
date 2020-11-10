build: clean_repo
	@make -B build_script
build_script:
	./build

push_to_gcp:
	./push

clean:
	find . -type f -name '*~' -delete -or -name '*#' -delete ;

clean_repo: clean
	./clean
