SELECT
    e.id,
    e.artist_id,
    e.venue_id,
    e.date,
    e.time,
    v.id,
    a.id 
FROM backlinebuilderapi_event e  
JOIN backlinebuilderapi_venue v 
    ON v.id = e.venue_id 
JOIN backlinebuilderapi_artist a 
    ON a.id = e.artist_id