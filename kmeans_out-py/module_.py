import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_

# Module: module_

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Main(noArgsParameter__):
        d_0_points_: _dafny.Array
        out0_: _dafny.Array
        out0_ = default__.MakePoints()
        d_0_points_ = out0_
        if not(default__.SameDim(d_0_points_)):
            raise _dafny.HaltException("KMeansTest.dfy(11,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        if not(((1) <= (default__.K)) and ((default__.K) <= ((d_0_points_).length(0)))):
            raise _dafny.HaltException("KMeansTest.dfy(12,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        d_1_initial__centroids_: _dafny.Array
        out1_: _dafny.Array
        out1_ = default__.DeterministicKMeansInitCentroids(d_0_points_, default__.K)
        d_1_initial__centroids_ = out1_
        if not(((d_1_initial__centroids_).length(0)) == (default__.K)):
            raise _dafny.HaltException("KMeansTest.dfy(18,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        if not(((d_1_initial__centroids_)[0]) == ((d_0_points_)[0])):
            raise _dafny.HaltException("KMeansTest.dfy(19,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        def lambda0_(forall_var_0_):
            d_2_c_: int = forall_var_0_
            return not (((0) <= (d_2_c_)) and ((d_2_c_) < (default__.K))) or ((((d_1_initial__centroids_)[d_2_c_]).length(0)) == (((d_0_points_)[0]).length(0)))

        if not(_dafny.quantifier(_dafny.IntegerRange(0, default__.K), True, lambda0_)):
            raise _dafny.HaltException("KMeansTest.dfy(20,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        def lambda1_(forall_var_1_):
            def lambda2_(exists_var_0_):
                d_4_i_: int = exists_var_0_
                return (((0) <= (d_4_i_)) and ((d_4_i_) < ((d_0_points_).length(0)))) and (((d_1_initial__centroids_)[d_3_c_]) == ((d_0_points_)[d_4_i_]))

            d_3_c_: int = forall_var_1_
            return not (((0) <= (d_3_c_)) and ((d_3_c_) < (default__.K))) or (_dafny.quantifier(_dafny.IntegerRange(0, (d_0_points_).length(0)), False, lambda2_))

        if not(_dafny.quantifier(_dafny.IntegerRange(0, default__.K), True, lambda1_)):
            raise _dafny.HaltException("KMeansTest.dfy(21,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        if not(((d_1_initial__centroids_).length(0)) >= (1)):
            raise _dafny.HaltException("KMeansTest.dfy(24,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        if not(((d_0_points_).length(0)) >= (default__.K)):
            raise _dafny.HaltException("KMeansTest.dfy(25,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        def lambda3_(forall_var_2_):
            def lambda4_(forall_var_3_):
                d_6_j_: int = forall_var_3_
                return not (((0) <= (d_6_j_)) and ((d_6_j_) < ((d_1_initial__centroids_).length(0)))) or ((((d_0_points_)[d_5_i_]).length(0)) == (((d_1_initial__centroids_)[d_6_j_]).length(0)))

            d_5_i_: int = forall_var_2_
            return not (((0) <= (d_5_i_)) and ((d_5_i_) < ((d_0_points_).length(0)))) or (_dafny.quantifier(_dafny.IntegerRange(0, (d_1_initial__centroids_).length(0)), True, lambda4_))

        if not(_dafny.quantifier(_dafny.IntegerRange(0, (d_0_points_).length(0)), True, lambda3_)):
            raise _dafny.HaltException("KMeansTest.dfy(26,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "initial centroids:\n"))).VerbatimString(False))
        d_7_ii_: int
        d_7_ii_ = 0
        while (d_7_ii_) < ((d_1_initial__centroids_).length(0)):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  cluster "))).VerbatimString(False))
            _dafny.print(_dafny.string_of(d_7_ii_))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ": "))).VerbatimString(False))
            d_8_id_: int
            d_8_id_ = 0
            while (d_8_id_) < (((d_1_initial__centroids_)[d_7_ii_]).length(0)):
                _dafny.print(_dafny.string_of(((d_1_initial__centroids_)[d_7_ii_])[d_8_id_]))
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " "))).VerbatimString(False))
                d_8_id_ = (d_8_id_) + (1)
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n"))).VerbatimString(False))
            d_7_ii_ = (d_7_ii_) + (1)
        d_9_centroids_: _dafny.Array
        d_10_labels_: _dafny.Array
        d_11_converged_: bool
        out2_: _dafny.Array
        out3_: _dafny.Array
        out4_: bool
        out2_, out3_, out4_ = default__.KMeans(d_0_points_, default__.K, d_1_initial__centroids_, default__.MaxIter)
        d_9_centroids_ = out2_
        d_10_labels_ = out3_
        d_11_converged_ = out4_
        if not(((d_10_labels_).length(0)) == ((d_0_points_).length(0))):
            raise _dafny.HaltException("KMeansTest.dfy(47,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        if not(((d_9_centroids_).length(0)) == (default__.K)):
            raise _dafny.HaltException("KMeansTest.dfy(48,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        def lambda5_(forall_var_4_):
            d_12_c_: int = forall_var_4_
            return not (((0) <= (d_12_c_)) and ((d_12_c_) < (default__.K))) or ((((d_9_centroids_)[d_12_c_]).length(0)) == (((d_0_points_)[0]).length(0)))

        if not(_dafny.quantifier(_dafny.IntegerRange(0, default__.K), True, lambda5_)):
            raise _dafny.HaltException("KMeansTest.dfy(49,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        def lambda6_(forall_var_5_):
            d_13_i_: int = forall_var_5_
            return not (((0) <= (d_13_i_)) and ((d_13_i_) < ((d_0_points_).length(0)))) or (((0) <= ((d_10_labels_)[d_13_i_])) and (((d_10_labels_)[d_13_i_]) < (default__.K)))

        if not(_dafny.quantifier(_dafny.IntegerRange(0, (d_0_points_).length(0)), True, lambda6_)):
            raise _dafny.HaltException("KMeansTest.dfy(50,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        def lambda7_(forall_var_6_):
            def lambda8_(forall_var_7_):
                d_15_c_: int = forall_var_7_
                return not (((0) <= (d_15_c_)) and ((d_15_c_) < (default__.K))) or ((default__.Dist2((d_0_points_)[d_14_i_], (d_9_centroids_)[(d_10_labels_)[d_14_i_]])) <= (default__.Dist2((d_0_points_)[d_14_i_], (d_9_centroids_)[d_15_c_])))

            d_14_i_: int = forall_var_6_
            return not (((0) <= (d_14_i_)) and ((d_14_i_) < ((d_0_points_).length(0)))) or (_dafny.quantifier(_dafny.IntegerRange(0, default__.K), True, lambda8_))

        if not(_dafny.quantifier(_dafny.IntegerRange(0, (d_0_points_).length(0)), True, lambda7_)):
            raise _dafny.HaltException("KMeansTest.dfy(51,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        def lambda9_(forall_var_8_):
            def lambda10_(forall_var_9_):
                d_17_j_: int = forall_var_9_
                return not (((0) <= (d_17_j_)) and ((d_17_j_) < (((d_0_points_)[0]).length(0)))) or (not ((default__.CountCluster(d_10_labels_, d_16_c_, (d_10_labels_).length(0))) > (0)) or ((((d_9_centroids_)[d_16_c_])[d_17_j_]) == ((default__.SumCoord(d_0_points_, d_10_labels_, d_16_c_, d_17_j_, (d_0_points_).length(0))) / (_dafny.BigRational(default__.CountCluster(d_10_labels_, d_16_c_, (d_10_labels_).length(0)), 1)))))

            d_16_c_: int = forall_var_8_
            return not (((0) <= (d_16_c_)) and ((d_16_c_) < (default__.K))) or (_dafny.quantifier(_dafny.IntegerRange(0, ((d_0_points_)[0]).length(0)), True, lambda10_))

        if not(not (d_11_converged_) or (_dafny.quantifier(_dafny.IntegerRange(0, default__.K), True, lambda9_))):
            raise _dafny.HaltException("KMeansTest.dfy(54,2): " + (_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "expectation violation"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "converged: "))).VerbatimString(False))
        _dafny.print(_dafny.string_of(d_11_converged_))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "labels: "))).VerbatimString(False))
        d_18_pi_: int
        d_18_pi_ = 0
        while (d_18_pi_) < ((d_10_labels_).length(0)):
            _dafny.print(_dafny.string_of((d_10_labels_)[d_18_pi_]))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " "))).VerbatimString(False))
            d_18_pi_ = (d_18_pi_) + (1)
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n"))).VerbatimString(False))
        _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "centroids:\n"))).VerbatimString(False))
        d_19_ci_: int
        d_19_ci_ = 0
        while (d_19_ci_) < ((d_9_centroids_).length(0)):
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "  cluster "))).VerbatimString(False))
            _dafny.print(_dafny.string_of(d_19_ci_))
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, ": "))).VerbatimString(False))
            d_20_di_: int
            d_20_di_ = 0
            while (d_20_di_) < (((d_9_centroids_)[d_19_ci_]).length(0)):
                _dafny.print(_dafny.string_of(((d_9_centroids_)[d_19_ci_])[d_20_di_]))
                _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, " "))).VerbatimString(False))
                d_20_di_ = (d_20_di_) + (1)
            _dafny.print((_dafny.SeqWithoutIsStrInference(map(_dafny.CodePoint, "\n"))).VerbatimString(False))
            d_19_ci_ = (d_19_ci_) + (1)

    @staticmethod
    def MakePoints():
        points: _dafny.Array = _dafny.Array(None, 0)
        nw0_ = _dafny.Array(_dafny.Array(None, 0), 100)
        points = nw0_
        nw1_ = _dafny.Array(None, 2)
        nw1_[int(0)] = _dafny.BigRational('2631858338e-9')
        nw1_[int(1)] = _dafny.BigRational('6893649044e-10')
        (points)[(0)] = nw1_
        nw2_ = _dafny.Array(None, 2)
        nw2_[int(0)] = _dafny.BigRational('808035174e-10')
        nw2_[int(1)] = _dafny.BigRational('46906898253e-10')
        (points)[(1)] = nw2_
        nw3_ = _dafny.Array(None, 2)
        nw3_[int(0)] = _dafny.BigRational('30025194892e-10')
        nw3_[int(1)] = _dafny.BigRational('7426535668e-10')
        (points)[(2)] = nw3_
        nw4_ = _dafny.Array(None, 2)
        nw4_[int(0)] = _dafny.BigRational('-637627769e-9')
        nw4_[int(1)] = _dafny.BigRational('40910470472e-10')
        (points)[(3)] = nw4_
        nw5_ = _dafny.Array(None, 2)
        nw5_[int(0)] = _dafny.BigRational('-722828865e-10')
        nw5_[int(1)] = _dafny.BigRational('28837693903e-10')
        (points)[(4)] = nw5_
        nw6_ = _dafny.Array(None, 2)
        nw6_[int(0)] = _dafny.BigRational('6283579292e-10')
        nw6_[int(1)] = _dafny.BigRational('44601362966e-10')
        (points)[(5)] = nw6_
        nw7_ = _dafny.Array(None, 2)
        nw7_[int(0)] = _dafny.BigRational('-26743726656e-10')
        nw7_[int(1)] = _dafny.BigRational('24800622166e-10')
        (points)[(6)] = nw7_
        nw8_ = _dafny.Array(None, 2)
        nw8_[int(0)] = _dafny.BigRational('-5774832063e-10')
        nw8_[int(1)] = _dafny.BigRational('30054335027e-10')
        (points)[(7)] = nw8_
        nw9_ = _dafny.Array(None, 2)
        nw9_[int(0)] = _dafny.BigRational('27275622784e-10')
        nw9_[int(1)] = _dafny.BigRational('13051254962e-10')
        (points)[(8)] = nw9_
        nw10_ = _dafny.Array(None, 2)
        nw10_[int(0)] = _dafny.BigRational('3419479849e-10')
        nw10_[int(1)] = _dafny.BigRational('39410461615e-10')
        (points)[(9)] = nw10_
        nw11_ = _dafny.Array(None, 2)
        nw11_[int(0)] = _dafny.BigRational('17053606407e-10')
        nw11_[int(1)] = _dafny.BigRational('44327702382e-10')
        (points)[(10)] = nw11_
        nw12_ = _dafny.Array(None, 2)
        nw12_[int(0)] = _dafny.BigRational('22065607593e-10')
        nw12_[int(1)] = _dafny.BigRational('55061671762e-10')
        (points)[(11)] = nw12_
        nw13_ = _dafny.Array(None, 2)
        nw13_[int(0)] = _dafny.BigRational('25209299612e-10')
        nw13_[int(1)] = _dafny.BigRational('-6385800263e-10')
        (points)[(12)] = nw13_
        nw14_ = _dafny.Array(None, 2)
        nw14_[int(0)] = _dafny.BigRational('25090492929e-10')
        nw14_[int(1)] = _dafny.BigRational('57731460973e-10')
        (points)[(13)] = nw14_
        nw15_ = _dafny.Array(None, 2)
        nw15_[int(0)] = _dafny.BigRational('-22716588353e-10')
        nw15_[int(1)] = _dafny.BigRational('20914437227e-10')
        (points)[(14)] = nw15_
        nw16_ = _dafny.Array(None, 2)
        nw16_[int(0)] = _dafny.BigRational('39228264819e-10')
        nw16_[int(1)] = _dafny.BigRational('18037083182e-10')
        (points)[(15)] = nw16_
        nw17_ = _dafny.Array(None, 2)
        nw17_[int(0)] = _dafny.BigRational('-16253565376e-10')
        nw17_[int(1)] = _dafny.BigRational('2254403975e-9')
        (points)[(16)] = nw17_
        nw18_ = _dafny.Array(None, 2)
        nw18_[int(0)] = _dafny.BigRational('1631237965e-10')
        nw18_[int(1)] = _dafny.BigRational('25775047251e-10')
        (points)[(17)] = nw18_
        nw19_ = _dafny.Array(None, 2)
        nw19_[int(0)] = _dafny.BigRational('-15951456185e-10')
        nw19_[int(1)] = _dafny.BigRational('4631224983e-9')
        (points)[(18)] = nw19_
        nw20_ = _dafny.Array(None, 2)
        nw20_[int(0)] = _dafny.BigRational('-26312873527e-10')
        nw20_[int(1)] = _dafny.BigRational('29700473406e-10')
        (points)[(19)] = nw20_
        nw21_ = _dafny.Array(None, 2)
        nw21_[int(0)] = _dafny.BigRational('-21705224161e-10')
        nw21_[int(1)] = _dafny.BigRational('6944791091e-10')
        (points)[(20)] = nw21_
        nw22_ = _dafny.Array(None, 2)
        nw22_[int(0)] = _dafny.BigRational('-15661868314e-10')
        nw22_[int(1)] = _dafny.BigRational('17497887636e-10')
        (points)[(21)] = nw22_
        nw23_ = _dafny.Array(None, 2)
        nw23_[int(0)] = _dafny.BigRational('-8867724871e-10')
        nw23_[int(1)] = _dafny.BigRational('1300926217e-9')
        (points)[(22)] = nw23_
        nw24_ = _dafny.Array(None, 2)
        nw24_[int(0)] = _dafny.BigRational('884843309e-10')
        nw24_[int(1)] = _dafny.BigRational('23229908592e-10')
        (points)[(23)] = nw24_
        nw25_ = _dafny.Array(None, 2)
        nw25_[int(0)] = _dafny.BigRational('9845148999e-10')
        nw25_[int(1)] = _dafny.BigRational('19521153869e-10')
        (points)[(24)] = nw25_
        nw26_ = _dafny.Array(None, 2)
        nw26_[int(0)] = _dafny.BigRational('21821796141e-10')
        nw26_[int(1)] = _dafny.BigRational('12996530234e-10')
        (points)[(25)] = nw26_
        nw27_ = _dafny.Array(None, 2)
        nw27_[int(0)] = _dafny.BigRational('1285351447e-9')
        nw27_[int(1)] = _dafny.BigRational('14369128512e-10')
        (points)[(26)] = nw27_
        nw28_ = _dafny.Array(None, 2)
        nw28_[int(0)] = _dafny.BigRational('8901176806e-10')
        nw28_[int(1)] = _dafny.BigRational('17984901469e-10')
        (points)[(27)] = nw28_
        nw29_ = _dafny.Array(None, 2)
        nw29_[int(0)] = _dafny.BigRational('-18960858512e-10')
        nw29_[int(1)] = _dafny.BigRational('26785030838e-10')
        (points)[(28)] = nw29_
        nw30_ = _dafny.Array(None, 2)
        nw30_[int(0)] = _dafny.BigRational('-755113462e-9')
        nw30_[int(1)] = _dafny.BigRational('37413864153e-10')
        (points)[(29)] = nw30_
        nw31_ = _dafny.Array(None, 2)
        nw31_[int(0)] = _dafny.BigRational('11203136497e-10')
        nw31_[int(1)] = _dafny.BigRational('57580608344e-10')
        (points)[(30)] = nw31_
        nw32_ = _dafny.Array(None, 2)
        nw32_[int(0)] = _dafny.BigRational('35435197152e-10')
        nw32_[int(1)] = _dafny.BigRational('2793552836e-9')
        (points)[(31)] = nw32_
        nw33_ = _dafny.Array(None, 2)
        nw33_[int(0)] = _dafny.BigRational('16416485407e-10')
        nw33_[int(1)] = _dafny.BigRational('1502088485e-10')
        (points)[(32)] = nw33_
        nw34_ = _dafny.Array(None, 2)
        nw34_[int(0)] = _dafny.BigRational('24703491517e-10')
        nw34_[int(1)] = _dafny.BigRational('40986290637e-10')
        (points)[(33)] = nw34_
        nw35_ = _dafny.Array(None, 2)
        nw35_[int(0)] = _dafny.BigRational('-19824365167e-10')
        nw35_[int(1)] = _dafny.BigRational('29353614204e-10')
        (points)[(34)] = nw35_
        nw36_ = _dafny.Array(None, 2)
        nw36_[int(0)] = _dafny.BigRational('8562407616e-10')
        nw36_[int(1)] = _dafny.BigRational('38623617483e-10')
        (points)[(35)] = nw36_
        nw37_ = _dafny.Array(None, 2)
        nw37_[int(0)] = _dafny.BigRational('8730512268e-10')
        nw37_[int(1)] = _dafny.BigRational('47143858294e-10')
        (points)[(36)] = nw37_
        nw38_ = _dafny.Array(None, 2)
        nw38_[int(0)] = _dafny.BigRational('13809348608e-10')
        nw38_[int(1)] = _dafny.BigRational('9294942182e-10')
        (points)[(37)] = nw38_
        nw39_ = _dafny.Array(None, 2)
        nw39_[int(0)] = _dafny.BigRational('24116339186e-10')
        nw39_[int(1)] = _dafny.BigRational('16042368281e-10')
        (points)[(38)] = nw39_
        nw40_ = _dafny.Array(None, 2)
        nw40_[int(0)] = _dafny.BigRational('-22664670096e-10')
        nw40_[int(1)] = _dafny.BigRational('44608968567e-10')
        (points)[(39)] = nw40_
        nw41_ = _dafny.Array(None, 2)
        nw41_[int(0)] = _dafny.BigRational('-4002680911e-10')
        nw41_[int(1)] = _dafny.BigRational('1837950753e-9')
        (points)[(40)] = nw41_
        nw42_ = _dafny.Array(None, 2)
        nw42_[int(0)] = _dafny.BigRational('24576091626e-10')
        nw42_[int(1)] = _dafny.BigRational('212853569e-9')
        (points)[(41)] = nw42_
        nw43_ = _dafny.Array(None, 2)
        nw43_[int(0)] = _dafny.BigRational('23535056956e-10')
        nw43_[int(1)] = _dafny.BigRational('22240495566e-10')
        (points)[(42)] = nw43_
        nw44_ = _dafny.Array(None, 2)
        nw44_[int(0)] = _dafny.BigRational('-7300001121e-10')
        nw44_[int(1)] = _dafny.BigRational('62545627227e-10')
        (points)[(43)] = nw44_
        nw45_ = _dafny.Array(None, 2)
        nw45_[int(0)] = _dafny.BigRational('11312175042e-10')
        nw45_[int(1)] = _dafny.BigRational('46819498471e-10')
        (points)[(44)] = nw45_
        nw46_ = _dafny.Array(None, 2)
        nw46_[int(0)] = _dafny.BigRational('4666178968e-10')
        nw46_[int(1)] = _dafny.BigRational('38657130258e-10')
        (points)[(45)] = nw46_
        nw47_ = _dafny.Array(None, 2)
        nw47_[int(0)] = _dafny.BigRational('11844703723e-10')
        nw47_[int(1)] = _dafny.BigRational('3188139952e-10')
        (points)[(46)] = nw47_
        nw48_ = _dafny.Array(None, 2)
        nw48_[int(0)] = _dafny.BigRational('13606996617e-10')
        nw48_[int(1)] = _dafny.BigRational('7480291196e-10')
        (points)[(47)] = nw48_
        nw49_ = _dafny.Array(None, 2)
        nw49_[int(0)] = _dafny.BigRational('-24397262387e-10')
        nw49_[int(1)] = _dafny.BigRational('40348985494e-10')
        (points)[(48)] = nw49_
        nw50_ = _dafny.Array(None, 2)
        nw50_[int(0)] = _dafny.BigRational('-10036273527e-10')
        nw50_[int(1)] = _dafny.BigRational('27463359301e-10')
        (points)[(49)] = nw50_
        nw51_ = _dafny.Array(None, 2)
        nw51_[int(0)] = _dafny.BigRational('6363319361e-10')
        nw51_[int(1)] = _dafny.BigRational('42544102108e-10')
        (points)[(50)] = nw51_
        nw52_ = _dafny.Array(None, 2)
        nw52_[int(0)] = _dafny.BigRational('14194214431e-10')
        nw52_[int(1)] = _dafny.BigRational('15740969549e-10')
        (points)[(51)] = nw52_
        nw53_ = _dafny.Array(None, 2)
        nw53_[int(0)] = _dafny.BigRational('689717142e-10')
        nw53_[int(1)] = _dafny.BigRational('43557327232e-10')
        (points)[(52)] = nw53_
        nw54_ = _dafny.Array(None, 2)
        nw54_[int(0)] = _dafny.BigRational('22635424995e-10')
        nw54_[int(1)] = _dafny.BigRational('18743026964e-10')
        (points)[(53)] = nw54_
        nw55_ = _dafny.Array(None, 2)
        nw55_[int(0)] = _dafny.BigRational('-20249364639e-10')
        nw55_[int(1)] = _dafny.BigRational('48474143152e-10')
        (points)[(54)] = nw55_
        nw56_ = _dafny.Array(None, 2)
        nw56_[int(0)] = _dafny.BigRational('-6700734013e-10')
        nw56_[int(1)] = _dafny.BigRational('2266856668e-9')
        (points)[(55)] = nw56_
        nw57_ = _dafny.Array(None, 2)
        nw57_[int(0)] = _dafny.BigRational('32340470926e-10')
        nw57_[int(1)] = _dafny.BigRational('7177388241e-10')
        (points)[(56)] = nw57_
        nw58_ = _dafny.Array(None, 2)
        nw58_[int(0)] = _dafny.BigRational('20657675422e-10')
        nw58_[int(1)] = _dafny.BigRational('26835341538e-10')
        (points)[(57)] = nw58_
        nw59_ = _dafny.Array(None, 2)
        nw59_[int(0)] = _dafny.BigRational('10220285958e-10')
        nw59_[int(1)] = _dafny.BigRational('41166034774e-10')
        (points)[(58)] = nw59_
        nw60_ = _dafny.Array(None, 2)
        nw60_[int(0)] = _dafny.BigRational('39384182185e-10')
        nw60_[int(1)] = _dafny.BigRational('-4500954012e-10')
        (points)[(59)] = nw60_
        nw61_ = _dafny.Array(None, 2)
        nw61_[int(0)] = _dafny.BigRational('7847825229e-10')
        nw61_[int(1)] = _dafny.BigRational('18670603681e-10')
        (points)[(60)] = nw61_
        nw62_ = _dafny.Array(None, 2)
        nw62_[int(0)] = _dafny.BigRational('-28197609229e-10')
        nw62_[int(1)] = _dafny.BigRational('31849331307e-10')
        (points)[(61)] = nw62_
        nw63_ = _dafny.Array(None, 2)
        nw63_[int(0)] = _dafny.BigRational('-23303136774e-10')
        nw63_[int(1)] = _dafny.BigRational('22283324836e-10')
        (points)[(62)] = nw63_
        nw64_ = _dafny.Array(None, 2)
        nw64_[int(0)] = _dafny.BigRational('-13602305178e-10')
        nw64_[int(1)] = _dafny.BigRational('35529136982e-10')
        (points)[(63)] = nw64_
        nw65_ = _dafny.Array(None, 2)
        nw65_[int(0)] = _dafny.BigRational('-30181616059e-10')
        nw65_[int(1)] = _dafny.BigRational('33572739626e-10')
        (points)[(64)] = nw65_
        nw66_ = _dafny.Array(None, 2)
        nw66_[int(0)] = _dafny.BigRational('16520905745e-10')
        nw66_[int(1)] = _dafny.BigRational('21201087303e-10')
        (points)[(65)] = nw66_
        nw67_ = _dafny.Array(None, 2)
        nw67_[int(0)] = _dafny.BigRational('17373078037e-10')
        nw67_[int(1)] = _dafny.BigRational('44254623439e-10')
        (points)[(66)] = nw67_
        nw68_ = _dafny.Array(None, 2)
        nw68_[int(0)] = _dafny.BigRational('-25271193606e-10')
        nw68_[int(1)] = _dafny.BigRational('13731111646e-10')
        (points)[(67)] = nw68_
        nw69_ = _dafny.Array(None, 2)
        nw69_[int(0)] = _dafny.BigRational('17437149893e-10')
        nw69_[int(1)] = _dafny.BigRational('9538290022e-10')
        (points)[(68)] = nw69_
        nw70_ = _dafny.Array(None, 2)
        nw70_[int(0)] = _dafny.BigRational('19263584961e-10')
        nw70_[int(1)] = _dafny.BigRational('41524301192e-10')
        (points)[(69)] = nw70_
        nw71_ = _dafny.Array(None, 2)
        nw71_[int(0)] = _dafny.BigRational('-6060451894e-10')
        nw71_[int(1)] = _dafny.BigRational('32366099143e-10')
        (points)[(70)] = nw71_
        nw72_ = _dafny.Array(None, 2)
        nw72_[int(0)] = _dafny.BigRational('32460247025e-10')
        nw72_[int(1)] = _dafny.BigRational('28494216528e-10')
        (points)[(71)] = nw72_
        nw73_ = _dafny.Array(None, 2)
        nw73_[int(0)] = _dafny.BigRational('-15767197373e-10')
        nw73_[int(1)] = _dafny.BigRational('49574059229e-10')
        (points)[(72)] = nw73_
        nw74_ = _dafny.Array(None, 2)
        nw74_[int(0)] = _dafny.BigRational('39782095479e-10')
        nw74_[int(1)] = _dafny.BigRational('23781784514e-10')
        (points)[(73)] = nw74_
        nw75_ = _dafny.Array(None, 2)
        nw75_[int(0)] = _dafny.BigRational('11940418364e-10')
        nw75_[int(1)] = _dafny.BigRational('2807728613e-9')
        (points)[(74)] = nw75_
        nw76_ = _dafny.Array(None, 2)
        nw76_[int(0)] = _dafny.BigRational('21156707631e-10')
        nw76_[int(1)] = _dafny.BigRational('30689615071e-10')
        (points)[(75)] = nw76_
        nw77_ = _dafny.Array(None, 2)
        nw77_[int(0)] = _dafny.BigRational('11536962208e-10')
        nw77_[int(1)] = _dafny.BigRational('39020063912e-10')
        (points)[(76)] = nw77_
        nw78_ = _dafny.Array(None, 2)
        nw78_[int(0)] = _dafny.BigRational('3038096308e-10')
        nw78_[int(1)] = _dafny.BigRational('39442341659e-10')
        (points)[(77)] = nw78_
        nw79_ = _dafny.Array(None, 2)
        nw79_[int(0)] = _dafny.BigRational('-18808979245e-10')
        nw79_[int(1)] = _dafny.BigRational('15429309679e-10')
        (points)[(78)] = nw79_
        nw80_ = _dafny.Array(None, 2)
        nw80_[int(0)] = _dafny.BigRational('24316930526e-10')
        nw80_[int(1)] = _dafny.BigRational('-2017371306e-10')
        (points)[(79)] = nw80_
        nw81_ = _dafny.Array(None, 2)
        nw81_[int(0)] = _dafny.BigRational('-2765252815e-10')
        nw81_[int(1)] = _dafny.BigRational('50812776833e-10')
        (points)[(80)] = nw81_
        nw82_ = _dafny.Array(None, 2)
        nw82_[int(0)] = _dafny.BigRational('10427873009e-10')
        nw82_[int(1)] = _dafny.BigRational('46062592252e-10')
        (points)[(81)] = nw82_
        nw83_ = _dafny.Array(None, 2)
        nw83_[int(0)] = _dafny.BigRational('17872641505e-10')
        nw83_[int(1)] = _dafny.BigRational('17001200557e-10')
        (points)[(82)] = nw83_
        nw84_ = _dafny.Array(None, 2)
        nw84_[int(0)] = _dafny.BigRational('-6539282684e-10')
        nw84_[int(1)] = _dafny.BigRational('4766569583e-9')
        (points)[(83)] = nw84_
        nw85_ = _dafny.Array(None, 2)
        nw85_[int(0)] = _dafny.BigRational('8821441163e-10')
        nw85_[int(1)] = _dafny.BigRational('28412848456e-10')
        (points)[(84)] = nw85_
        nw86_ = _dafny.Array(None, 2)
        nw86_[int(0)] = _dafny.BigRational('14201333113e-10')
        nw86_[int(1)] = _dafny.BigRational('46374616548e-10')
        (points)[(85)] = nw86_
        nw87_ = _dafny.Array(None, 2)
        nw87_[int(0)] = _dafny.BigRational('9480878502e-10')
        nw87_[int(1)] = _dafny.BigRational('4732119198e-9')
        (points)[(86)] = nw87_
        nw88_ = _dafny.Array(None, 2)
        nw88_[int(0)] = _dafny.BigRational('465464941e-9')
        nw88_[int(1)] = _dafny.BigRational('31231551433e-10')
        (points)[(87)] = nw88_
        nw89_ = _dafny.Array(None, 2)
        nw89_[int(0)] = _dafny.BigRational('26693468918e-10')
        nw89_[int(1)] = _dafny.BigRational('18198703315e-10')
        (points)[(88)] = nw89_
        nw90_ = _dafny.Array(None, 2)
        nw90_[int(0)] = _dafny.BigRational('5889432611e-10')
        nw90_[int(1)] = _dafny.BigRational('40014845769e-10')
        (points)[(89)] = nw90_
        nw91_ = _dafny.Array(None, 2)
        nw91_[int(0)] = _dafny.BigRational('16201139697e-10')
        nw91_[int(1)] = _dafny.BigRational('27469273884e-10')
        (points)[(90)] = nw91_
        nw92_ = _dafny.Array(None, 2)
        nw92_[int(0)] = _dafny.BigRational('24512742341e-10')
        nw92_[int(1)] = _dafny.BigRational('-1953978488e-10')
        (points)[(91)] = nw92_
        nw93_ = _dafny.Array(None, 2)
        nw93_[int(0)] = _dafny.BigRational('-4272444173e-10')
        nw93_[int(1)] = _dafny.BigRational('35731459921e-10')
        (points)[(92)] = nw93_
        nw94_ = _dafny.Array(None, 2)
        nw94_[int(0)] = _dafny.BigRational('-2561146855e-9')
        nw94_[int(1)] = _dafny.BigRational('35994767796e-10')
        (points)[(93)] = nw94_
        nw95_ = _dafny.Array(None, 2)
        nw95_[int(0)] = _dafny.BigRational('-28428114237e-10')
        nw95_[int(1)] = _dafny.BigRational('24562976565e-10')
        (points)[(94)] = nw95_
        nw96_ = _dafny.Array(None, 2)
        nw96_[int(0)] = _dafny.BigRational('-3388742209e-10')
        nw96_[int(1)] = _dafny.BigRational('32348248733e-10')
        (points)[(95)] = nw96_
        nw97_ = _dafny.Array(None, 2)
        nw97_[int(0)] = _dafny.BigRational('12893377802e-10')
        nw97_[int(1)] = _dafny.BigRational('34496915881e-10')
        (points)[(96)] = nw97_
        nw98_ = _dafny.Array(None, 2)
        nw98_[int(0)] = _dafny.BigRational('18407062774e-10')
        nw98_[int(1)] = _dafny.BigRational('3561622307e-9')
        (points)[(97)] = nw98_
        nw99_ = _dafny.Array(None, 2)
        nw99_[int(0)] = _dafny.BigRational('-9016725622e-10')
        nw99_[int(1)] = _dafny.BigRational('13158246057e-10')
        (points)[(98)] = nw99_
        nw100_ = _dafny.Array(None, 2)
        nw100_[int(0)] = _dafny.BigRational('-27523395321e-10')
        nw100_[int(1)] = _dafny.BigRational('37622452377e-10')
        (points)[(99)] = nw100_
        return points

    @staticmethod
    def Dist2Prefix(v1, v2, n):
        d_0___accumulator_ = _dafny.BigRational('0e0')
        while True:
            with _dafny.label():
                if (n) == (0):
                    return (_dafny.BigRational('0e0')) + (d_0___accumulator_)
                elif True:
                    d_0___accumulator_ = ((((v1)[(n) - (1)]) - ((v2)[(n) - (1)])) * (((v1)[(n) - (1)]) - ((v2)[(n) - (1)]))) + (d_0___accumulator_)
                    in0_ = v1
                    in1_ = v2
                    in2_ = (n) - (1)
                    v1 = in0_
                    v2 = in1_
                    n = in2_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def Dist2(v1, v2):
        return default__.Dist2Prefix(v1, v2, (v1).length(0))

    @staticmethod
    def SquaredEuclideanDistance(v1, v2):
        sum_: _dafny.BigRational = _dafny.BigRational()
        d_0_i_: int
        d_0_i_ = 0
        sum_ = _dafny.BigRational('0e0')
        while (d_0_i_) < ((v1).length(0)):
            d_1_diff_: _dafny.BigRational
            d_1_diff_ = ((v1)[d_0_i_]) - ((v2)[d_0_i_])
            sum_ = (sum_) + ((d_1_diff_) * (d_1_diff_))
            d_0_i_ = (d_0_i_) + (1)
        return sum_

    @staticmethod
    def AssignLabels(points, centroids):
        labels: _dafny.Array = _dafny.Array(None, 0)
        d_0_n_: int
        d_0_n_ = (points).length(0)
        d_1_k_: int
        d_1_k_ = (centroids).length(0)
        nw0_ = _dafny.Array(int(0), d_0_n_)
        labels = nw0_
        d_2_p__i_: int
        d_2_p__i_ = 0
        while (d_2_p__i_) < (d_0_n_):
            d_3_i_: int
            d_3_i_ = d_2_p__i_
            d_4_p_: _dafny.Array
            d_4_p_ = (points)[d_3_i_]
            d_5_best__i_: int
            d_5_best__i_ = 0
            d_6_best__d_: _dafny.BigRational
            d_6_best__d_ = default__.Dist2(d_4_p_, (centroids)[0])
            d_7_c__i_: int
            d_7_c__i_ = 1
            while (d_7_c__i_) < (d_1_k_):
                d_8_d_: _dafny.BigRational
                d_8_d_ = default__.Dist2(d_4_p_, (centroids)[d_7_c__i_])
                if (d_8_d_) < (d_6_best__d_):
                    d_6_best__d_ = d_8_d_
                    d_5_best__i_ = d_7_c__i_
                d_7_c__i_ = (d_7_c__i_) + (1)
            (labels)[(d_3_i_)] = d_5_best__i_
            d_2_p__i_ = (d_2_p__i_) + (1)
        labels = labels
        return labels
        return labels

    @staticmethod
    def CountCluster(labels, c, n):
        d_0___accumulator_ = 0
        while True:
            with _dafny.label():
                if (n) == (0):
                    return (0) + (d_0___accumulator_)
                elif True:
                    d_0___accumulator_ = ((1 if ((labels)[(n) - (1)]) == (c) else 0)) + (d_0___accumulator_)
                    in0_ = labels
                    in1_ = c
                    in2_ = (n) - (1)
                    labels = in0_
                    c = in1_
                    n = in2_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def SumCoord(points, labels, c, j, n):
        d_0___accumulator_ = _dafny.BigRational('0e0')
        while True:
            with _dafny.label():
                if (n) == (0):
                    return (_dafny.BigRational('0e0')) + (d_0___accumulator_)
                elif True:
                    d_0___accumulator_ = ((((points)[(n) - (1)])[j] if ((labels)[(n) - (1)]) == (c) else _dafny.BigRational('0e0'))) + (d_0___accumulator_)
                    in0_ = points
                    in1_ = labels
                    in2_ = c
                    in3_ = j
                    in4_ = (n) - (1)
                    points = in0_
                    labels = in1_
                    c = in2_
                    j = in3_
                    n = in4_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def UpdateCentroids(points, labels, k, old__centroids):
        new__centroids: _dafny.Array = _dafny.Array(None, 0)
        d_0_n_: int
        d_0_n_ = (points).length(0)
        d_1_d_: int
        d_1_d_ = ((points)[0]).length(0)
        d_2_sums_: _dafny.Array
        nw0_ = _dafny.Array(_dafny.BigRational(), k, d_1_d_)
        d_2_sums_ = nw0_
        d_3_counts_: _dafny.Array
        nw1_ = _dafny.Array(int(0), k)
        d_3_counts_ = nw1_
        d_4_c_: int
        d_4_c_ = 0
        while (d_4_c_) < (k):
            (d_3_counts_)[(d_4_c_)] = 0
            d_5_r_: int
            d_5_r_ = 0
            while (d_5_r_) < (d_1_d_):
                (d_2_sums_)[(d_4_c_), (d_5_r_)] = _dafny.BigRational('0e0')
                d_5_r_ = (d_5_r_) + (1)
            d_4_c_ = (d_4_c_) + (1)
        d_6_i_: int
        d_6_i_ = 0
        while (d_6_i_) < (d_0_n_):
            d_7_lab_: int
            d_7_lab_ = (labels)[d_6_i_]
            (d_3_counts_)[(d_7_lab_)] = ((d_3_counts_)[d_7_lab_]) + (1)
            d_8_j_: int
            d_8_j_ = 0
            while (d_8_j_) < (d_1_d_):
                (d_2_sums_)[(d_7_lab_), (d_8_j_)] = ((d_2_sums_)[d_7_lab_, d_8_j_]) + (((points)[d_6_i_])[d_8_j_])
                d_8_j_ = (d_8_j_) + (1)
            d_6_i_ = (d_6_i_) + (1)
        nw2_ = _dafny.Array(_dafny.Array(None, 0), k)
        new__centroids = nw2_
        d_4_c_ = 0
        while (d_4_c_) < (k):
            d_9_centroid_: _dafny.Array
            nw3_ = _dafny.Array(_dafny.BigRational(), d_1_d_)
            d_9_centroid_ = nw3_
            if ((d_3_counts_)[d_4_c_]) == (0):
                d_10_j_: int
                d_10_j_ = 0
                while (d_10_j_) < (d_1_d_):
                    (d_9_centroid_)[(d_10_j_)] = ((old__centroids)[d_4_c_])[d_10_j_]
                    d_10_j_ = (d_10_j_) + (1)
            elif True:
                d_11_inv_: _dafny.BigRational
                d_11_inv_ = (_dafny.BigRational('1e0')) / (_dafny.BigRational((d_3_counts_)[d_4_c_], 1))
                d_12_j_: int
                d_12_j_ = 0
                while (d_12_j_) < (d_1_d_):
                    (d_9_centroid_)[(d_12_j_)] = ((d_2_sums_)[d_4_c_, d_12_j_]) * (d_11_inv_)
                    d_12_j_ = (d_12_j_) + (1)
            (new__centroids)[(d_4_c_)] = d_9_centroid_
            d_4_c_ = (d_4_c_) + (1)
        return new__centroids

    @staticmethod
    def LabelsEqual(new__labels, old__labels):
        result: bool = False
        d_0_n_: int
        d_0_n_ = (new__labels).length(0)
        d_1_i_: int
        d_1_i_ = 0
        while (d_1_i_) < (d_0_n_):
            if ((new__labels)[d_1_i_]) != ((old__labels)[d_1_i_]):
                result = False
                return result
            d_1_i_ = (d_1_i_) + (1)
        result = True
        return result
        return result

    @staticmethod
    def KMeans(points, k, initial__centroids, max__iterations):
        centroids: _dafny.Array = _dafny.Array(None, 0)
        labels: _dafny.Array = _dafny.Array(None, 0)
        converged: bool = False
        centroids = initial__centroids
        out0_: _dafny.Array
        out0_ = default__.AssignLabels(points, centroids)
        labels = out0_
        converged = False
        d_0_it_: int
        d_0_it_ = 0
        while (d_0_it_) < (max__iterations):
            d_1_old__labels_: _dafny.Array
            d_1_old__labels_ = labels
            out1_: _dafny.Array
            out1_ = default__.UpdateCentroids(points, d_1_old__labels_, k, centroids)
            centroids = out1_
            d_2_new__labels_: _dafny.Array
            out2_: _dafny.Array
            out2_ = default__.AssignLabels(points, centroids)
            d_2_new__labels_ = out2_
            out3_: bool
            out3_ = default__.LabelsEqual(d_2_new__labels_, d_1_old__labels_)
            converged = out3_
            if converged:
                labels = d_1_old__labels_
                converged = True
                return centroids, labels, converged
            labels = d_2_new__labels_
            d_0_it_ = (d_0_it_) + (1)
        return centroids, labels, converged

    @staticmethod
    def SameDim(points):
        def lambda0_(forall_var_0_):
            def lambda1_(forall_var_1_):
                d_1_j_: int = forall_var_1_
                return not ((((0) <= (d_0_i_)) and ((d_0_i_) <= (d_1_j_))) and ((d_1_j_) < ((points).length(0)))) or ((((points)[d_0_i_]).length(0)) == (((points)[d_1_j_]).length(0)))

            d_0_i_: int = forall_var_0_
            return _dafny.quantifier(_dafny.IntegerRange(d_0_i_, (points).length(0)), True, lambda1_)

        return (((points).length(0)) >= (1)) and (_dafny.quantifier(_dafny.IntegerRange(0, ((points).length(0)) + (1)), True, lambda0_))

    @staticmethod
    def ValidIdxs(n, idxs):
        def lambda0_(forall_var_0_):
            d_0_t_: int = forall_var_0_
            return not (((0) <= (d_0_t_)) and ((d_0_t_) < (len(idxs)))) or (((0) <= ((idxs)[d_0_t_])) and (((idxs)[d_0_t_]) < (n)))

        return _dafny.quantifier(_dafny.IntegerRange(0, len(idxs)), True, lambda0_)

    @staticmethod
    def MinDistIdx(points, p, chosen):
        if (len(chosen)) == (1):
            return default__.Dist2((points)[p], (points)[(chosen)[0]])
        elif True:
            d_0_prev_ = default__.MinDistIdx(points, p, _dafny.SeqWithoutIsStrInference((chosen)[:(len(chosen)) - (1):]))
            d_1_curr_ = default__.Dist2((points)[p], (points)[(chosen)[(len(chosen)) - (1)]])
            if (d_0_prev_) < (d_1_curr_):
                return d_0_prev_
            elif True:
                return d_1_curr_

    @staticmethod
    def FindFarthestIndex(points, chosen):
        best: int = int(0)
        best = 0
        d_0_i_: int
        d_0_i_ = 1
        while (d_0_i_) < ((points).length(0)):
            if (default__.MinDistIdx(points, best, chosen)) < (default__.MinDistIdx(points, d_0_i_, chosen)):
                best = d_0_i_
            d_0_i_ = (d_0_i_) + (1)
        return best

    @staticmethod
    def DeterministicInitIdxs(points, k):
        idxs: _dafny.Seq = _dafny.Seq({})
        idxs = _dafny.SeqWithoutIsStrInference([0])
        while (len(idxs)) < (k):
            d_0_oldIdxs_: _dafny.Seq
            d_0_oldIdxs_ = idxs
            d_1_next_: int
            out0_: int
            out0_ = default__.FindFarthestIndex(points, d_0_oldIdxs_)
            d_1_next_ = out0_
            idxs = (d_0_oldIdxs_) + (_dafny.SeqWithoutIsStrInference([d_1_next_]))
        return idxs

    @staticmethod
    def MaterializeCentroids(points, idxs):
        centroids: _dafny.Array = _dafny.Array(None, 0)
        nw0_ = _dafny.Array(_dafny.Array(None, 0), len(idxs))
        centroids = nw0_
        d_0_t_: int
        d_0_t_ = 0
        while (d_0_t_) < (len(idxs)):
            (centroids)[(d_0_t_)] = (points)[(idxs)[d_0_t_]]
            d_0_t_ = (d_0_t_) + (1)
        return centroids

    @staticmethod
    def DeterministicKMeansInit(points, k):
        idxs: _dafny.Seq = _dafny.Seq({})
        centroids: _dafny.Array = _dafny.Array(None, 0)
        out0_: _dafny.Seq
        out0_ = default__.DeterministicInitIdxs(points, k)
        idxs = out0_
        out1_: _dafny.Array
        out1_ = default__.MaterializeCentroids(points, idxs)
        centroids = out1_
        return idxs, centroids

    @staticmethod
    def DeterministicKMeansInitCentroids(points, k):
        centroids: _dafny.Array = _dafny.Array(None, 0)
        d_0_idxs_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = default__.DeterministicInitIdxs(points, k)
        d_0_idxs_ = out0_
        out1_: _dafny.Array
        out1_ = default__.MaterializeCentroids(points, d_0_idxs_)
        centroids = out1_
        return centroids

    @_dafny.classproperty
    def K(instance):
        return 3
    @_dafny.classproperty
    def MaxIter(instance):
        return 100
