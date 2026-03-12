"""
PDFDownloader - Model Layer

Currently contains a class for the manipulation of Excel files.
Also contains an interface class in order to be able to easily switch
out the concrete implementation.

At this prototype level of the software, Excel files are used as database
and user interface, as this is seemingly what the client's employees prefer
to work with.
"""

import logging
from abc import ABC, abstractmethod
from typing import Tuple
import pandas as pd

# System setup
log = logging.getLogger(__name__)

class ExcelFile(ABC):
    """
    Interface for an Excel file.
    Should be initialized with its file name,
    and provide access to at least two functions,
    for reading data and for manipulation of data.
    """

    @abstractmethod
    def __init__( self, filepath: String ) -> None:
        """Initialize with file path and keep this value"""

    @abstractmethod
    def load_dataframe( self, columns: list[int] ) -> pd.DataFrame:
        """Load all data from the columns specified"""

    @abstractmethod
    def append_row( self, data: pd.DataFrame, sheet: String ) ->\
        df.DataFrame:
        """
        Append new row to file on the sheet specified;
        Create new file/sheet if needed.
        """

class ExcelFileImplementation:
    """Implementation of ExcelFile interface"""

    def __init__( self, filepath: String ) -> None:
        """Initialize with file path and keep this value"""

        if str(filepath):
            self.filepath = filepath
        else:
            self.filepath = ""

    def load_columns( columns: list[int] ) -> pd.DataFrame:
        """
        Reads specified columns from an Excel file.

        Args:
            columns: List of column indices to read

        Returns:
            pd.DataFrame: DataFrame with the specified columns

        Example usage:
            data = load_columns([ 1, 2, 3 ])
        """
        df = pd.read_excel(file_path, usecols=column_names)
        return df

    def append_row( data: pd.DataFrame, sheet='Sheet1' ):
        """
        Appends new data rows to an Excel file.

        Args:
            data (pd.DataFrame): Data to append
            sheet_name (str):    Target sheet name

        Returns:
            new_df: DataFrame that was added to the Excel file

        Example usage:
            new_rows = [{'Name': 'Alice', 'Age': 30}, {'Name': 'Bob', 'Age': 25}]
            new_dataframe = pd.DataFrame( new_rows )
            append_row( 'data.xlsx', new_dataframe )
        """

        # Convert to DataFrame if needed
        if not isinstance(data, pd.DataFrame):
            new_df = pd.DataFrame(data)
        else:
            new_df = data

        if os.path.exists(self.file_path):
            # Read existing data
            existing_df = pd.read_excel( file_path, sheet_name=sheet )
            # Combine and save
            combined_df = pd.concat( [existing_df, new_df], ignore_index=True )
            combined_df.to_excel( file_path, sheet_name=sheet, index=False )
        else:
            # Create new file
            new_df.to_excel( file_path, sheet_name=sheet, index=False )

        return new_df
