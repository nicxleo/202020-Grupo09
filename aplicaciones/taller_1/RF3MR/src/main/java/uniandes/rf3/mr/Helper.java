package uniandes.rf3.mr;

/**
 *
 * @author Esteb
 */
public class Helper {

    public static IndexEntity GetIndex(String[] pLstColumna) {

        Boolean vFirst;
        try {
            Integer.parseInt(pLstColumna[0]);
            vFirst = true;
        } catch (NumberFormatException e) {
            vFirst = false;
        }
        Boolean vSecond;
        try {
            Integer.parseInt(pLstColumna[3]);
            vSecond = true;
        } catch (NumberFormatException e) {
            vSecond = false;
        }

        IndexEntity vIndexEntity = new IndexEntity();
        if (vFirst && vSecond) {
            vIndexEntity.Tipo = "yellow";
            vIndexEntity.ZonaDesde = 7;
            vIndexEntity.ZonaHasta = 8;
            vIndexEntity.FechaDesde = 1;
            vIndexEntity.FechaHasta = 2;
            vIndexEntity.MontoTotal = 16;
        }
        if (vFirst && !vSecond) {
            vIndexEntity.Tipo = "green";
            vIndexEntity.ZonaDesde = 5;
            vIndexEntity.ZonaHasta = 6;
            vIndexEntity.FechaDesde = 1;
            vIndexEntity.FechaHasta = 2;
            vIndexEntity.MontoTotal = 16;
        }
        if (!vFirst) {
            vIndexEntity.Tipo = "fhv";
            vIndexEntity.ZonaDesde = 3;
            vIndexEntity.ZonaHasta = 4;
            vIndexEntity.FechaDesde = 1;
            vIndexEntity.FechaHasta = 2;
            vIndexEntity.MontoTotal = -1;
        }

        return vIndexEntity;
    }
}
