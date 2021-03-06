IMAGE_NAME_APP := sweetmusic_app
IMAGE_NAME_LB := sweetmusic_lb
IMAGE_NAME_DB := sweetmusic_db
DOCKER_HUB_USERNAME := kristineadomingo
FILES :=        \
    .gitignore  \
    .travis.yml \
    makefile    \
    apiary.apib \
    IDB3.log    \
    models.html \
    app/models.py   \
    app/tests.py    \
    UML.pdf

check:
	@not_found=0;                                 \
    for i in $(FILES);                            \
    do                                            \
        if [ -e $$i ];                            \
        then                                      \
            echo "$$i found";                     \
        else                                      \
            echo "$$i NOT FOUND";                 \
            not_found=`expr "$$not_found" + "1"`; \
        fi                                        \
    done;                                         \
    if [ $$not_found -ne 0 ];                     \
    then                                          \
        echo "$$not_found failures";              \
        exit 1;                                   \
    fi;                                           \
    echo "success";

clean:
	rm -rf app/__pycache__
	rm -rf __pycache__

test:
	python3 app/tests.py

docker-build:
	@if [ -z "$$CONTINUE" ]; then \
		read -r -p "Have you sourced the !!!! MAIN !!!! docker.env file for our Carina cluster? (y/n): " CONTINUE; \
	fi ; \
	[ $$CONTINUE = "y" ] || [ $$CONTINUE = "Y" ] || (echo "Exiting."; exit 1;)
	@echo "Building the images..."
	docker login

	docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_APP} app
	docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_APP}

	docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_LB} lb
	docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_LB}

	docker build -t ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_DB} db 
	docker push ${DOCKER_HUB_USERNAME}/${IMAGE_NAME_DB}

init-db:
	docker-compose --file docker-compose-prod.yml run -d --rm --no-deps app python idb.py create_db

docker-push:
	 docker-compose --file docker-compose-prod.yml up -d

docker-proxy:
	docker run -it --rm \
	--name temp-proxy \
	--net cs373idb_backend \
	--publish 3306:3306 \
	--env PROTOCOL=TCP \
	--env UPSTREAM=sweetmusic_db \
	--env UPSTREAM_PORT=3306 \
	carinamarina/nginx-proxy
