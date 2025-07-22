#!/bin/bash

cd StoneDetector

./gradlew jar

java -Xms8G -Xmx8G -jar build/libs/StoneDetector.jar -x --directory="test/JHotDraw" --error-file=errors.txt > results.txt