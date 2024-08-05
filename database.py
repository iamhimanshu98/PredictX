import sqlite3
conn = sqlite3.connect("flight_user_data.db")

conn.execute("""
                    create table userrecord(
                        name varchar(40),
                        age int,
                        gender int,
                        flight_distance int,
                        arrival_delay int,
                        departure_delay int,
                        inflight_entertainment int,
                        baggage_handling int,
                        cleanliness int,
                        customer_type int,
                        travel_type int,
                        flight_class text,
                        class_eco int,
                        class_eco_plus int
                        )
                """)


print("Table created successfully in database!")

conn.commit()
conn.close