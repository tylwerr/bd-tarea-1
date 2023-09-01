CREATE FUNCTION calcularTasa (@suma_wins INT, @suma_games INT)
RETURNS FLOAT
AS
BEGIN
    DECLARE @tasa FLOAT;
    SET @tasa = ( @suma_wins * 100.0 ) / @suma_games;
    RETURN @tasa
END;