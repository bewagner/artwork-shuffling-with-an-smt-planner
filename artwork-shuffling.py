from dataclasses import dataclass
from itertools import combinations

import z3
from z3 import Int


@dataclass
class Artwork:
    name: str
    start_room: int
    end_room: int


if __name__ == "__main__":
    artworks = [
        Artwork("Girl with a Pearl Earring", 1, 2),
        Artwork("Mona Lisa", 0, 1),
        Artwork("The Kiss", 2, 3),
    ]

    index_variables = {artwork.name: Int(artwork.name) for artwork in artworks}

    solver = z3.Solver()

    for artwork in artworks:
        index_variable = index_variables[artwork.name]

        solver.add(index_variable >= 0)
        solver.add(index_variable < len(artworks))

    for combination in combinations(artworks, 2):
        first_artwork = combination[0]
        second_artwork = combination[1]

        first_variable = index_variables[first_artwork.name]
        second_variable = index_variables[second_artwork.name]

        solver.add(first_variable != second_variable)

        if first_artwork.end_room == second_artwork.start_room:
            solver.add(second_variable < first_variable)

        if second_artwork.end_room == first_artwork.start_room:
            solver.add(first_variable < second_variable)

    if solver.check() != z3.sat:
        print("Solving the artwork assignment problem failed!")
        exit(1)

    model = solver.model()
    indices = [
        model.evaluate(index_variables[artwork.name]).as_long() for artwork in artworks
    ]
    print(indices)
    print(solver)
    result = [artworks[i] for i in indices]

    print(result)
