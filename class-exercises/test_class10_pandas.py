#test_class10_pandas.py
import pandas as pd

def test_dataframe_shape():
    # This DataFrame has 5 rows and 4 columns.
    df = pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })

    # assert checks a condition. If it is true, the test continues. If it is false, the test fails.
    assert df.shape == (5, 4)
    # assert df.shape == (1, 1) 
    # ^ will get an AssertionError


#test_class10_pandas.py

def test_drop_duplicates():
    # Arrange
    df = pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })
    # note: the final two rows are identical, so removing duplicates leaves four rows and four columns.

    # Act
    result = df.drop_duplicates()

    # Assert
    assert result.shape == (4, 4)
    assert result["title"].tolist() == ["Movie A", "Movie B", "Movie C", "Movie D"]


#`test_class10_pandas.py`
import pytest 

def test_invalid_numeric_value():
    df = pd.DataFrame({"rating": [7, "unknown", 9]})

    with pytest.raises(ValueError):
        pd.to_numeric(df["rating"])


#test_class10_pandas.py

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "title": ["Movie A", "Movie B", "Movie C", "Movie D", "Movie D"],
        "type": ["Movie", "Movie", "Movie", "Movie", "Movie"],
        "release_year": [2020, 2021, 2022, 2023, 2023],
        "rating": [7, 8, 6, 9, 9],
    })


def test_dataframe_shape(sample_df): # just sample_df instead of sample_df()
    assert sample_df.shape == (5, 4)

def test_drop_duplicates(sample_df):
    result = sample_df.drop_duplicates()
    assert result.shape == (4, 4)
    assert result["title"].tolist() == ["Movie A", "Movie B", "Movie C", "Movie D"]