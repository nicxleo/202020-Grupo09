package uniandes.ra1.mr;

import java.util.Date;

/**
 *
 * @author Esteb
 */
public class ViajeEntity {

    private Double Distancia;
    private int MedioPago;
    private Double ValorPagado;
    private Date FechaEntrada;
    private Date FechaSalida;
    private int CantidadPasajeros;
    private int DistanciaXPrecio;

    public Double getDistancia() {
        return Distancia;
    }

    public void setDistancia(Double Distancia) {
        this.Distancia = Distancia;
    }

    public int getMedioPago() {
        return MedioPago;
    }

    public void setMedioPago(int MedioPago) {
        this.MedioPago = MedioPago;
    }

    public Double getValorPagado() {
        return ValorPagado;
    }

    public void setValorPagado(Double ValorPagado) {
        this.ValorPagado = ValorPagado;
    }

    public Date getFechaEntrada() {
        return FechaEntrada;
    }

    public void setFechaEntrada(Date FechaEntrada) {
        this.FechaEntrada = FechaEntrada;
    }

    public Date getFechaSalida() {
        return FechaSalida;
    }

    public void setFechaSalida(Date FechaSalida) {
        this.FechaSalida = FechaSalida;
    }

    public int getCantidadPasajeros() {
        return CantidadPasajeros;
    }

    public void setCantidadPasajeros(int CantidadPasajeros) {
        this.CantidadPasajeros = CantidadPasajeros;
    }

    public int getDistanciaXPrecio() {
        return DistanciaXPrecio;
    }

    public void setDistanciaXPrecio(int DistanciaXPrecio) {
        this.DistanciaXPrecio = DistanciaXPrecio;
    }
}
