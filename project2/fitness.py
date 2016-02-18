

class OneMaxFitness(object):
    @staticmethod
    def evaluate(phenotype):
        return sum(phenotype.data)


class LolzFitness(object):
    ZERO_CAP = 4

    @staticmethod
    def evaluate(phenotype):
        zero_score = 0
        one_score = 0
        zero_streak = True
        one_streak = True

        for x in phenotype.data:
            if x == 0 and zero_streak:
                zero_score += 1
                one_streak = False
            elif x == 1 and one_streak:
                one_score += 1
                zero_streak = False
            else:
                break

        if zero_score > LolzFitness.ZERO_CAP:
            zero_score = LolzFitness.ZERO_CAP

        return max(zero_score, one_score)


class SurprisingSequencesFitness(object):
    @staticmethod
    def evaluate(phenotype):
        pass  # TODO
