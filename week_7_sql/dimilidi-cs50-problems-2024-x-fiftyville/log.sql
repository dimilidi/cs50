-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Find crime scene description - 10:15am, bakery, littering at 16:36
SELECT description
FROM crime_scene_reports
WHERE month = 7 AND day = 28
    AND street = 'Humphrey Street';


-- Find some clue in the bakery - who left within 10 min after 10:25am on  28.07.2023
SELECT *
FROM bakery_security_logs
WHERE year = 2023
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute BETWEEN 15 AND 25
    AND activity LIKE 'exit';

-- -> 5P2BI95, 94KL13X, 6P58WS2, 4328GD8, G412CB7, L93JTIZ, 322W7JE, 0NTHK55

SELECT *
FROM people p
WHERE p.license_plate  IN (
    SELECT bsl.license_plate
    FROM bakery_security_logs bsl)
JOIN bank_accounts ba ON p.id = ba.person_id
JOIN atm_transactions atm ON atm.account_number = ba.account_number
WHERE atm.year = 2023 AND atm.month = 7 AND atm.day = 28
     AND atm_location = 'Leggett Street';



-- Find interviews transcript
SELECT *
FROM interviews
WHERE month = 7 AND day = 28;
-- -> thief get into a car at bakery parking lot sometime within ten minutes of the theft - between 10:15 and 10:25 (Ruth)
-- -> thief was on Leggett Street at ATM earlier in the morning (Eugene)
-- -> thief if flying tommorow (29.07) - earliest fligh (Raymond)
-- -> thief calles s.o. for less than a minute (Raymond)


-- Find out who have made transaction at ATM earlier in the morning  on Leggett Street --> account number
SELECT *
FROM atm_transactions
WHERE year = 2023 AND month = 7 AND day = 28
    AND atm_location = 'Leggett Street';

-- Find people that:
    -- withdraw money at ATM and
    -- left the bakery within 10 min after theft and
    -- made a less than 1 min call and
    -- is going to fly early on 29.07
SELECT p.name, p.phone_number, p.passport_number, p.license_plate
FROM people p
JOIN bank_accounts ba ON p.id = ba.person_id
JOIN atm_transactions atm ON atm.account_number = ba.account_number
JOIN passengers pssgr ON  p.passport_number = pssgr.passport_number
WHERE atm.year = 2023
    AND atm.month = 7
    AND atm.day = 28
    AND atm.atm_location LIKE 'Leggett Street'
    AND atm.transaction_type LIKE 'withdraw'
    AND p.license_plate IN (
        SELECT bsl.license_plate
        FROM bakery_security_logs bsl
        WHERE year = 2023
            AND month = 7
            AND day = 28
            AND hour = 10
            AND minute BETWEEN 15 AND 25
            AND activity LIKE 'exit'
        )
    AND p.phone_number IN (
        SELECT caller
        FROM phone_calls pc
        WHERE pc.year = 2023
            AND pc.month = 7
            AND pc.day = 28
            AND pc.duration < 60
    AND p.passport_number IN (
        SELECT  p.passport_number
        FROM flights f
        JOIN airports a ON f.origin_airport_id = a.id
        JOIN passengers p ON f.id = p.flight_id
        WHERE f.year = 2023
            AND f.month = 7
            AND  f.day = 29
            AND a.city LIKE 'Fiftyville'
            AND f.hour = (
                SELECT MIN(f1.hour)
                FROM flights f1
                JOIN airports a1 ON f1.origin_airport_id = a1.id
                WHERE f1.year = 2023
                    AND f1.month = 7
                    AND f1.day = 29
                    AND a1.city LIKE 'Fiftyville'
                )
            )
    );

-- -> Bruce 94KL13X,  5773159633, (367) 555-5533 ;

-- -> Diana 322W7JE, 3592750733, (770) 555-1861


-- FIND phone calls < 1 min, caller
SELECT caller, receiver
FROM phone_calls
WHERE year = 2023
    AND month = 7
    AND day = 28
    AND duration < 60;


-- Find passengers on earliest flight from Fiftyville on 29.07
SELECT  p.passport_number, DISTINCT f.destination_airport_id
FROM flights f
JOIN airports a ON f.origin_airport_id = a.id
JOIN passengers p ON f.id = p.flight_id
WHERE f.year = 2023
    AND f.month = 7
    AND  f.day = 29
    AND a.city LIKE 'Fiftyville'
    AND f.hour = (
      SELECT MIN(f1.hour)
      FROM flights f1
      JOIN airports a1 ON f1.origin_airport_id = a1.id
      WHERE f1.year = 2023
        AND f1.month = 7
        AND f1.day = 29
        AND a1.city LIKE 'Fiftyville'
  );


-- Find earliest flight from Fiftyville on 29.07
SELECT MIN(f.hour)
FROM flights f
JOIN airports a ON f.origin_airport_id = a.id
WHERE f.year = 2023
    AND f.month = 7
    AND  f.day = 29
    AND a.city LIKE 'Fiftyville';



-- Find escape city
SELECT DISTINCT a.city
FROM airports a
JOIN flights f ON a.id = f.destination_airport_id
WHERE f.id = (
    SELECT f1.id
    FROM flights f1
    JOIN airports a1 ON f1.origin_airport_id = a1.id
    WHERE f1.year = 2023
      AND f1.month = 7
      AND f1.day = 29
      AND a1.city LIKE 'Fiftyville'
    ORDER BY f1.hour ASC
    LIMIT 1
);

-- -> New York City

-- Find accomplice
SELECT p.name, pc.caller, pc.receiver, pc.year, pc.month, pc.day,  pc.duration, p2.name as accomplice
FROM phone_calls pc
JOIN people p ON pc.caller = p.phone_number
JOIN people p2 ON pc.receiver = p2.phone_number
WHERE pc.year = 2023
    AND pc.month = 7
    AND pc.day = 28
    AND pc.duration < 60
    AND p.name LIKE 'Bruce';
