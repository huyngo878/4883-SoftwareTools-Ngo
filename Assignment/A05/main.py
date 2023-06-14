import json


def createDotFile():
  with open("dwarf_family_tree.json") as f:
    data = json.load(f)

  with open("graph.dot", "w") as f:
    f.write("digraph DwarfClans {\n")
    f.write("node [shape=plaintext]\n")

    # Create a dictionary where each clan is a key and the value is a list of people in that clan
    clanDict = {}
    for person in data:
      clanName = person['clanName']
      if clanName not in clanDict:
        clanDict[clanName] = []
      clanDict[clanName].append(person)

    # For each clan, create a subgraph and add the people in that clan to the subgraph
    for clan, people in clanDict.items():
      f.write(f'subgraph cluster_{clan.replace(" ", "_")} {{\n')
      f.write(f'label = "{clan}"\n')

      for person in people:
        for person in people:
            color = "blue" if person["gender"] == "M" else "pink"
            table = f'''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{color}">
                           <TR><TD>Name</TD><TD>{person["fname"]} {person["lname"]}</TD></TR>
                           <TR><TD>Born-Died</TD><TD>{person["birthDate"]}-{person["deathDate"]}</TD></TR>
                           <TR><TD>Age</TD><TD>{person["age"]}</TD></TR>
                           <TR><TD>Gender</TD><TD>{person["gender"]}</TD></TR>
                           </TABLE>>'''
            f.write(f'"{person["id"]}" [label={table}]\n')

      f.write('}\n')

    # Create an edge between each person and their spouse
    for person in data:
      if person["spouseId"]:
        f.write(
          f'"{person["id"]}" -- "{person["spouseId"]}" [color=blue, dir=none]\n'
        )

    # Create an edge between each person and their parents
    for person in data:
      if person["fatherId"]:
        f.write(
          f'"{person["fatherId"]}" -- "{person["id"]}" [color=red, dir=back]\n'
        )
      if person["motherId"]:
        f.write(
          f'"{person["motherId"]}" -- "{person["id"]}" [color=red, dir=back]\n'
        )

    f.write("}\n")


if __name__ == '__main__':
  createDotFile()
