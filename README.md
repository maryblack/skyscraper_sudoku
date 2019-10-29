# Skyscraper sudoku

In a grid of 6 by 6 squares you need to place a skyscraper in each square with only some clues:

 - The height of the skyscrapers is between 1 and 6
 - No two skyscrapers in a row or column may have the same number of floors
 - A clue is the number of skyscrapers that you can see in a row or column from the outside
 - Higher skyscrapers block the view of lower skyscrapers located behind them

To understand how the puzzle works, this is an example of a row with 2 clues. Seen from the left there are 6 buildings visible while seen from the right side only 1:

| 6 |   |   |   |   |   |   | 1 |
| - |:-:|:-:|:-:|:-:|:-:|:-:|:-:|

There is only one way in which the skyscrapers can be placed. From left-to-right all six buildings must be visible and no building may hide behind another building:

|6| 1 | 2 | 3 | 4 | 5 | 6 | 1 |
|-|-|-|-|-|-|-|-|


### Task:

Input: The clues in an array of 24 items ordered around the clock. Index:

| |**0**|**1**|**2**|**3**|**4**|**5**| |
|-|-|-|-|-|-|-|-|
|**23**| | | | | | |**6**|
|**22**| | | | | | |**7**|
|**21**| | | | | | |**8**|
|**20**| | | | | | |**9**|
|**19**| | | | | | |**10**|
|**18**| | | | | | |**11**|
| |**17**|**16**|**15**|**14**|**13**|**12**| |

 - If no clue is available, add value `0`
 - Each puzzle has only one possible solution
 
 Output: Array of skyscrapers heights linewise (top to bottom, left to right).

### Example of a 6 by 6 puzzle with the solution:

| | | | |**2**|**2**| | |
|-|-|-|-|-|-|-|-|
| |5|6|1|4|3|2| |
| |4|1|3|2|6|5| |
|**3**|2|3|6|1|5|4| |
| |6|5|4|3|2|1|**6**|
|**4**|1|2|5|6|4|3|**3**|
|**4**|3|4|2|5|1|6| | 
| | | | | |**4**| | |  

Input: `'0,0,0,2,2,0,0,0,0,6,3,0,0,4,0,0,0,0,4,4,0,3,0,0'`

Output: `'5,6,1,4,3,2,4,1,3,2,6,5,2,3,6,1,5,4,6,5,4,3,2,1,1,2,5,6,4,3,3,4,2,5,1,6'`
