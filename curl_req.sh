#!/bin/bash
for i in {1..500}
do
    echo $i

    curl --location --request POST 'http://localhost:3000/audit' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYmFzaWxpbmpvZSIsImV4cCI6MTY0ODU3MTA5OX0.uChrcu59oPcDAc8Q2LWL16-xB0HCTQrd2K6coE12CAQ' \
    --header 'Content-Type: application/json' \
    --data-raw '{
                "id":"roshnipeter",
                "action":"buy",
                "action_doc" : {"skuId":"'"B${i}"'"}
                 }'

    curl --location --request GET 'http://127.0.0.1:3000/audit?id=roshnipeter&action=buy' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYmFzaWxpbmpvZSIsImV4cCI6MTY0ODU3MTA5OX0.uChrcu59oPcDAc8Q2LWL16-xB0HCTQrd2K6coE12CAQ' \
    --data-raw ''

    curl --location --request GET 'http://127.0.0.1:3000/audit?id=roshnipeter&action=sell' \
    --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYmFzaWxpbmpvZSIsImV4cCI6MTY0ODU3MTA5OX0.uChrcu59oPcDAc8Q2LWL16-xB0HCTQrd2K6coE12CAQ' \
    --data-raw ''
done