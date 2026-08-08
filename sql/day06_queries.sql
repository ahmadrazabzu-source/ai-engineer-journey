-- =========================================================
-- Day 6 — SQL Fundamentals with SQLite
-- Dataset: UCI Heart Failure Clinical Records
-- Database: healthcare_analytics.db
-- Main table: heart_failure_records
-- Lookup table: outcome_lookup
-- Purpose: Practice analytical SQL using cleaned healthcare data
-- =========================================================


-- =========================================================
-- Q1. How many records are in the table?
-- Skills: SELECT, COUNT, alias
-- =========================================================

SELECT
    COUNT(*) AS total_records
FROM heart_failure_records;


-- =========================================================
-- Q2. How many records belong to each death-event category?
-- Skills: GROUP BY, COUNT, ORDER BY
-- =========================================================

SELECT
    death_event,
    COUNT(*) AS record_count
FROM heart_failure_records
GROUP BY death_event
ORDER BY death_event;


-- =========================================================
-- Q3. What is the average age for each death-event category?
-- Skills: GROUP BY, COUNT, AVG, ROUND
-- =========================================================

SELECT
    death_event,
    COUNT(*) AS record_count,
    ROUND(AVG(age), 2) AS mean_age
FROM heart_failure_records
GROUP BY death_event
ORDER BY death_event;


-- =========================================================
-- Q4. Which records have age >= 65 and diabetes recorded?
-- Skills: WHERE, AND, ORDER BY, LIMIT
-- =========================================================

SELECT
    age,
    diabetes,
    ejection_fraction,
    serum_creatinine,
    death_event
FROM heart_failure_records
WHERE age >= 65
  AND diabetes = 1
ORDER BY age DESC
LIMIT 10;


-- =========================================================
-- Q5. What are the five highest serum-creatinine observations?
-- Skills: SELECT, ORDER BY, DESC, LIMIT
-- =========================================================

SELECT
    age,
    serum_creatinine,
    serum_sodium,
    ejection_fraction,
    death_event
FROM heart_failure_records
ORDER BY serum_creatinine DESC
LIMIT 5;


-- =========================================================
-- Q6. Compare several averages between death-event groups.
-- Skills: GROUP BY, multiple aggregates, aliases
-- =========================================================

SELECT
    death_event,
    COUNT(*) AS n,
    ROUND(AVG(age), 2) AS mean_age,
    ROUND(AVG(ejection_fraction), 2) AS mean_ejection_fraction,
    ROUND(AVG(serum_creatinine), 2) AS mean_serum_creatinine,
    ROUND(AVG(serum_sodium), 2) AS mean_serum_sodium
FROM heart_failure_records
GROUP BY death_event
ORDER BY death_event;


-- =========================================================
-- Q7. How are diabetes and death-event categories distributed?
-- Skills: multi-column GROUP BY, COUNT, ORDER BY
-- =========================================================

SELECT
    diabetes,
    death_event,
    COUNT(*) AS record_count
FROM heart_failure_records
GROUP BY
    diabetes,
    death_event
ORDER BY
    diabetes,
    death_event;


-- =========================================================
-- Q8. Join observations to descriptive outcome labels.
-- Skills: INNER JOIN, aliases, ON, GROUP BY
-- =========================================================

SELECT
    o.outcome_label,
    COUNT(*) AS record_count,
    ROUND(AVG(h.age), 2) AS mean_age
FROM heart_failure_records AS h
INNER JOIN outcome_lookup AS o
    ON h.death_event = o.death_event
GROUP BY o.outcome_label
ORDER BY o.outcome_label;


-- =========================================================
-- Q9. How many records have serum creatinine
-- above the overall dataset average?
-- Skills: subquery, AVG, WHERE, COUNT
-- =========================================================

SELECT
    COUNT(*) AS records_above_mean_creatinine
FROM heart_failure_records
WHERE serum_creatinine >
    (
        SELECT AVG(serum_creatinine)
        FROM heart_failure_records
    );


-- =========================================================
-- Q10. Compare death-event counts among records
-- below the overall mean ejection fraction.
-- Skills: subquery, WHERE, GROUP BY, COUNT, ROUND
-- =========================================================

SELECT
    death_event,
    COUNT(*) AS record_count,
    ROUND(AVG(ejection_fraction), 2) AS mean_ejection_fraction
FROM heart_failure_records
WHERE ejection_fraction <
    (
        SELECT AVG(ejection_fraction)
        FROM heart_failure_records
    )
GROUP BY death_event
ORDER BY death_event;