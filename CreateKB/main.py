from openai import OpenAI
from proposition import Response, AtomDescription
from pydantic import BaseModel
from typing import List


class Atoms(BaseModel):
    atoms: List[AtomDescription]

    def update(self, atoms: List[AtomDescription]):
        self.atoms.extend(atoms)


def get_text(filename):
    with open(filename, "r") as f:
        knowledge = f.read()
    return knowledge


client = OpenAI(api_key="sk-proj-vU744CvQVK2ffqWQQlbFT3BlbkFJRp54HFS3Lhyb6h0G83Au")


def logic_of(knowledge: str, atoms: Atoms):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful logician. Convert the user input into propositional logic, giving both the final proposition as well as a list of atoms.",
            },
            {
                "role": "user",
                "content": f"Convert the following knowledge into propositional logic: {knowledge} \n \n. Here are the atoms we have already defined: {atoms.model_dump_json()}",
            },
        ],
        response_format=Response,
    )
    kb = completion.choices[0].message.parsed
    return kb


def convert_and_save(name: str, atoms: Atoms):
    text = get_text(f"{name}.txt")
    logic = logic_of(text, atoms)
    atoms.update(logic.atom_descriptions)
    with open(f"../ProveML/{name}.json", "w") as f:
        f.write(logic.model_dump_json(indent=2))


if __name__ == "__main__":
    atoms = Atoms(atoms=[])
    convert_and_save("knowledge", atoms)
    convert_and_save("query", atoms)
