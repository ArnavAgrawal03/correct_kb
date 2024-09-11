from typing import List, Union, Dict
from pydantic import BaseModel


# Define base class for Proposition
class Prop(BaseModel):
    pass


# Define all possible types of propositions
class Atom(Prop):
    value: str


class Or(Prop):
    left_or: Prop
    right_or: Prop


class And(Prop):
    left_and: Prop
    right_and: Prop


class Not(Prop):
    operand_not: Prop


class Imp(Prop):
    left_imp: Prop
    right_imp: Prop


class Iff(Prop):
    left_iff: Prop
    right_iff: Prop


class Proposition(BaseModel):
    child: Union[Atom, Or, And, Not, Imp, Iff]


# Rebuild models to enable recursive types
Proposition.model_rebuild()


# Response model containing the proposition and a list of atoms
class Response(BaseModel):
    proposition: List[Proposition]
    atoms: Dict[str, Atom]  # List of atom strings extracted from the proposition
