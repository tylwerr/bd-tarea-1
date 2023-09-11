/* 
calcularTasa
————————
@suma_wins: float
@suma_games: float
————————
Se calcula la tasa apartir de la suma total de partidos ganados dividido por la
suma total de partidos jugados, luego se multiplica por 100 para sacar el porcentaje.
Se retorna float el resultado anterior.
*/
CREATE FUNCTION calcularTasa
(
@suma_wins float,
@suma_games float
)
RETURNS float
AS
BEGIN
    DECLARE @tasa float
    SET @tasa = ( @suma_wins * 100.0 ) / @suma_games
    RETURN @tasa
END
