# seed_countries.py
import pycountry, pyodbc

cnxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER=ANIER-PC\\A3ERP;DATABASE=KratosDB;UID=sa;PWD=Asd123$%;TrustServerCertificate=yes")
cur = cnxn.cursor()

# # Tabla: COUNTRIES(country_code CHAR(2) PK, name NVARCHAR(100))
# rows = [(c.alpha_2, c.name) for c in pycountry.countries if hasattr(c, "alpha_2")]
# cur.fast_executemany = True
# cur.executemany("MERGE dbo.COUNTRIES AS T USING (VALUES (?,?)) AS S(code,name) " 
#                 "ON T.country_code = S.code "
#                 "WHEN NOT MATCHED THEN INSERT(country_code,name) VALUES(S.code,S.name);", rows)
# cnxn.commit()
# cur.close(); cnxn.close()
# print("Países insertados/actualizados")

# Tabla: SUBDIVISIONS(country_code CHAR(2), subdivision_code NVARCHAR(10), name NVARCHAR(150), PK(country_code, subdivision_code))
rows = []
for s in pycountry.subdivisions:
    # s.code ej: 'ES-M'; country_code es lo que hay antes del guion
    cc, sub = s.code.split('-', 1)
    rows.append((cc, s.code, s.name))

cur.fast_executemany = True
cur.executemany("""
MERGE dbo.SUBDIVISIONS AS T
USING (VALUES (?,?,?)) AS S(country_code, subdivision_code, name)
ON T.country_code = S.country_code AND T.subdivision_code = S.subdivision_code
WHEN NOT MATCHED THEN INSERT(country_code, subdivision_code, name) VALUES(S.country_code, S.subdivision_code, S.name)
WHEN MATCHED AND T.name <> S.name THEN UPDATE SET name = S.name;
""", rows)
cnxn.commit()
cur.close(); cnxn.close()
print("Subdivisiones insertadas/actualizadas")


