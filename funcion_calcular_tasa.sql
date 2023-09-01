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