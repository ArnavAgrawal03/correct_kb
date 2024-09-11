from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel


class PropType(str, Enum):
    ATOM = "atom"
    OR = "or"
    AND = "and"
    NOT = "not"
    IMP = "imp"
    IFF = "iff"


class Atom(BaseModel):
    value: str


class SingleAttribute(BaseModel):
    prop: "Proposition"


class LRAttributes(BaseModel):
    left_prop: "Proposition"
    right_prop: "Proposition"


class Proposition(BaseModel):
    type: PropType
    attributes: Union[LRAttributes, SingleAttribute, Atom]


class AtomDescription(BaseModel):
    atom: Atom
    description: str


Proposition.model_rebuild()


class Response(BaseModel):
    proposition: Proposition
    atom_descriptions: List[AtomDescription]
    # atoms: Dict[str, Atom]  # List of atom strings extracted from the proposition

    def _convert_single_prop(self, prop: Proposition, convert):
        match (prop.type):
            case PropType.ATOM:
                return convert[prop.attributes.value]
            case PropType.OR:
                left_repr = self._convert_single_prop(prop.attributes.left_prop, convert=convert)
                right_repr = self._convert_single_prop(prop.attributes.right_prop, convert=convert)
                return f"({left_repr} or {right_repr})"
            case PropType.AND:
                left_repr = self._convert_single_prop(prop.attributes.left_prop, convert=convert)
                right_repr = self._convert_single_prop(prop.attributes.right_prop, convert=convert)
                return f"({left_repr} and {right_repr})"
            case PropType.NOT:
                return f"not {self._convert_single_prop(prop.attributes.prop, convert=convert)}"
            case PropType.IMP:
                left_repr = self._convert_single_prop(prop.attributes.left_prop, convert=convert)
                right_repr = self._convert_single_prop(prop.attributes.right_prop, convert=convert)
                return f"({left_repr} -> {right_repr})"
            case PropType.IFF:
                left_repr = self._convert_single_prop(prop.attributes.left_prop, convert=convert)
                right_repr = self._convert_single_prop(prop.attributes.right_prop, convert=convert)
                return f"({left_repr} <-> {right_repr})"

    def _get_atom_dict(self):
        d = {atom.atom.value: atom.description for atom in self.atom_descriptions}
        return d

    def __repr__(self) -> str:
        convert = self._get_atom_dict()
        props = [self._convert_single_prop(prop, convert) for prop in self.proposition]
        return "\n".join(props)
