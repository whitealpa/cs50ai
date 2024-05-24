from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    Or(AKnight, AKnave), # A is either a knight or a knave
    Implication(AKnight, And(AKnight, AKnave)), # If A is a knight (speaking truth), then A is both a knight and a knave
    Implication(AKnave, Not(And(AKnight, AKnave))) # If A is a knave (speaking lie), then A is not both a knight and a knave
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    Or(AKnight, AKnave), # A is either a knight or a knave
    Or(BKnight, BKnave), # B is either a knight or a knave
    
    Implication(AKnight, And(AKnight, BKnight)), # If A is a knight, both of them must be knaves
    Implication(AKnave, Not(And(AKnave, BKnave))), # If A is a knave, not both of them are knaves
    
    Implication(BKnight, Not(AKnight)), # If B is not a knave, then A is not a knight
    Implication(BKnave, AKnave) #If B is knave, then A must be a knave too
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    Or(AKnight, AKnave), # A is either a knight or a knave
    Or(BKnight, BKnave), # B is either a knight or a knave

    Implication(AKnight, And(AKnight, BKnight)), # If A is a knight, both of them must be knights
    Implication(AKnave, Not(And(AKnave, BKnave))), # If A is a knave, both of them cannot be knaves
    
    Implication(BKnight, Not(AKnight)), # If B is a knight, then A cannot be a knight
    Implication(BKnave, AKnave), # If B is a knave, then B must be a knave
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    Or(AKnight, AKnave), # A is either a knight or a knave
    Or(BKnight, BKnave), # B is either a knight or a knave
    Or(CKnight, CKnave), # C is either a knight or a knave
    
    Implication(AKnight, BKnave), # If A is a knight, B must be a knave
    Implication(AKnave, CKnave), # If A is a knave, C must be a knave
    
    And(Implication(BKnight, AKnave), Implication(AKnave, BKnave)), # If B is a knight, A must be a knave, and if A is a knave, B must be lying that A said 'I am a knave'
    
    Implication(BKnight, Not(And(AKnight, CKnight))), # If B is a knight, A and C cannot be knights
    Implication(BKnave, And(AKnight, CKnight)), # If B is a knave, A and C must be knights
    
    Implication(CKnight, AKnight), # If C is a knight, A must be a knight

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
