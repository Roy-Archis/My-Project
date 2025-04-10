import pickle


names_to_remove = {
    'shayan', 'shayan1', 'shayanchakraborty',
    'shay', 'shy', 'chando', 'mishu', 'shayan chakraborty', 'chakraborty'
}


with open('./data/names.pkl', 'rb') as f:
    data = pickle.load(f)


if isinstance(data, list):
    filtered_data = [name for name in data if str(name).strip().lower() not in names_to_remove]
else:
    raise TypeError(f"Expected a list in names.pkl, but got {type(data)}")


with open('./data/names.pkl', 'wb') as f:
    pickle.dump(filtered_data, f)


