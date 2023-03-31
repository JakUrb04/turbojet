# Tutaj znajdują się skrypty z obliczeniami
import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Union



# Funkcje do obliczania podstawowych parametrów, takich jak spręż, podgrzew itd.

def pressure_ratio(pressure_one: Union[int,float,list,tuple],pressure_two: Union[int,float]=None)->float:
    """Funkcja służy do obliczania sprężu
    :param pressure_one: Ciśnienie przed obiektem (sprężarka, komora spalania itd.) [Pa]
    :param pressure_two: Ciśnienie za obiektem (sprężarka, komora spalania itd.) [Pa]
    """
    if isinstance(pressure_one,(tuple,list)):
        pressure_one, pressure_two = pressure_one
    compress = pressure_two/pressure_one
    return compress

def temperature_ratio(temperature_one: Union[int,float,list,tuple],temperature_two: Union[int,float]=None)->float:
    """Funkcja służy do obliczania podgrzewu
    :param temperature_one: Temperatura przed obiektem (np. komora spalania) [K]
    :param temperature_two: Temperatura za obiektem (np. komora spalania) [K]
    """
    if isinstance(temperature_one,(list,tuple)):
        temperature_one, temperature_two = temperature_one
    heat = temperature_two/temperature_one
    return heat

def individual_gas_constant(M: Union[int,float])->Union[int,float]:
    """Funkcja zwraca indywidualną stałą gazową R [J/kmol*K]
    :param M: Masa cząsteczkowa gazu [kg/kmol]
    """
    R = 8314.7/M
    return R 

# Obliczanie podstawowych zależności związanych z atmosferą wzorcową (ISA)
class StandardAtmosphere:
    def standard_temperature(self, height: Union[int,float])->Union[int,float]:
        """Funkcja zwraca temperaturę zgodną z ISA na danej wysokości [K]
        :param height: Wysokość [m]
        """
        if height < 11000:
            t = 288.15 - 0.0065 * height
        elif height >= 11000 and height <= 20000:
            t = 216.65
        else:
            raise ValueError("Wysokość nie może być większa niż 20000 metrów!")
        return t
    
    def standard_pressure(self, height: Union[int,float])->Union[int,float]:
        """Funkcja zwraca ciśnienie zgodne z ISA na danej wysokości [Pa]
        :param height: Wysokość [m]
        """
        if height < 11000:
            p = 101325 * (1 - height / 44300) ** 5.256
        elif height >= 11000 and height <= 20000:
            p = 22064 * math.exp((height - 11000) / 6340)
        else:
            raise ValueError("Wysokość nie może być większa niż 20000 metrów!")
        return p

# Klasa reprezentująca sprężarkę odrzutowego silnika turbinowego
class Compressor:
    def temperature_one(self,T: Union[int,float,tuple,list],k: Union[int,float]=None,M: Union[int,float]=None)->float:
        """Funkcja zwraca temperaturę na wlocie do sprężarki [K]
        :param T: Temperatura [K] lub lista/krotka z wartościami: (Temperatura [K], Wykładnik izentropy, Liczba Macha)
        :param k: Wykładnik izentropy
        :param M: Liczba Macha
        """
        if isinstance(T,(tuple,list)):
            T, k, M = T
        temp = T*(1+(k-1)/2*M**2)
        return temp

    def pressure_one(self,inlet_compress: Union[int,float,tuple,list],standard_pressure: Union[int,float]=None,
    k: Union[int,float]=None, M: Union[int,float]=None)->float:
        """Funkcja zwraca ciśnienie przed sprężarką [Pa]
        :param inlet_compress: Spręż wlotu
        :param standard_pressure: Ciśnienie na wysokości zgodne z ISA [Pa]
        :param k: Wykładnik izentropy
        :param M: Liczba Macha
        """
        if isinstance(inlet_compress,(tuple,list)):
            inlet_compress, standard_pressure, k, M = inlet_compress
        p = inlet_compress*standard_pressure*(1+((k-1)/2)*M**2)**(k/(k-1))
        return p

    def compressor_work(k: Union[int,float,list,tuple],R: Union[int,float]=None,temperature_one: Union[int,float]=None,
    compressor_compress: Union[int,float]=None,compression_efficiency: Union[int,float]=None)->float:
        """Funkcja zwraca pracę sprężarki [J]
        :param k: Wykładnik izentropy
        :param R: Indywidualna stała gazowa [J/kg*K]
        :param temperature_one: Temperatura przed sprężarką [K]
        :param compressor_compress: Spręż sprężarki
        :param compression_efficiency: Sprawność sprężarki
        """
        if isinstance(k,(tuple,list)):
            k, R, temperature_one, compressor_compress, compression_efficiency = k
        L = ((k*R)/(k-1))*temperature_one*((compressor_compress**((k-1)/k)-1)/compression_efficiency)
        return L

    def temperature_two_fw(self,temperature_one: Union[int,float,list,tuple],k: Union[int,float]=None,
    R: Union[int,float]=None,compressor_work: Union[int,float]=None)->float:
        """Funkcja pozwala na obliczenie temperatury za sprężarką [K]
        :param temperature_one: Temperatura przed sprężarką [K]
        :param k: Wykładnik izentropy
        :param R: Indywidualna stała gazowa
        :param compressor_work: Praca sprężarki [J]
        """
        if isinstance(temperature_one,(list,tuple)):
            temperature_one, k, R, compressor_work = temperature_one
        temperature_two = temperature_one + compressor_work*((k-1)/(k*R))
        return temperature_two

class CombustionChamber:
    def cumks(self,temperature_two: Union[int,float,list,tuple],
    temperature_three: Union[int,float]=None) -> float: # Te nazwę zmienić, jak się dowiem
        """Funkcja pozwala na obliczenie CUMKS
        :param temperature_two: Temperatura przed komorą spalania [K]
        :param temperature_three: Temperatura za komorą spalania [K]
        """
        if isinstance(temperature_two,(list,tuple)):
            temperature_two, temperature_three = temperature_two
        
        c = 1000*(0.9089+0.0002095*(temperature_three+0.48*temperature_two))
        return c
    
    def relative_fuel_consumption(self,cumks: Union[int,float,list,tuple],temperature_three: Union[int,float]=None,
    temperature_two: Union[int,float]=None,heat_release_coefficient: Union[int,float]=None, Wd: Union[int,float]=None)->float:
        """Funkcja pozwala obliczyć względne zużycie paliwa
        :param cumks: To niewiadomo co na razie
        :param temperature_three: Temperatura za komorą spalania [K]
        :param temperature_two: Temperatura przed komorą spalania [K]
        :param heat_release_coefficient: Współczynnik wydzielenia ciepła w KS
        :param Wd: Też niewiadomo co na razie
        """
        if isinstance(cumks,(tuple,list)):
            cumks,temperature_three, temperature_two, heat_release_coefficient, Wd = cumks
        tau = cumks*((temperature_three-temperature_two)/(heat_release_coefficient*Wd))
        return tau

    def excess_air_factor(self,tau: Union[int,float,list,tuple],Ltpow: Union[int,float]=None)->float:
        """Funkcja pozwala obliczyć współczynnik nadmiaru powietrza
        :param tau: Względne zużycie paliwa [JEDNOSTKA]
        :param Ltpow: Jakaś praca, ale jaka? [J]            
        """                                                         # Poopisywać to potem dobrze
        if isinstance(tau,(tuple,list)):
            tau, Ltpow = tau
        a = 1/(tau*Ltpow)
        return a

    def pressure_three(self,pressure_two: Union[int,float,tuple,list],
    combustion_chamber_compress: Union[int,float]=None)->float:
        """Funkcja pozwala obliczyć ciśnienie p3 (ciśnienie przed turbiną) z p2 i sprężem
        """
        if isinstance(pressure_two,(list,tuple)):
            pressure_two,combustion_chamber_compress = pressure_two
        p_3 = pressure_two*combustion_chamber_compress
        return p_3
