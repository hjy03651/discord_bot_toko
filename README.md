# discord_bot_toko (v120)
## info
- Codes for Discord bots for accessing psql and for use on **private servers**.
- Variations of the code are allowed.
- It'll be deleted at any time if there are any probs.

## explanation
- `dbclass_main`: for accessing the main schema.
- `dbtool_book`: book return/loan/add/modify/delete in conjunction with 'dbclass_main'.
- `dbclass_events`: code for accessing the event schema.
- `dbtool_events`: collecting and calculating information about generated events.
- `embedding`: default value of the success/error message output frame.
- `ids`: book id generation code.
- `inuitoko_v120`: main. not yet modulated.

## DBs
### public
- book: `book_id` | `title` | `series` | `byname1` | `byname2` | `location` | `can_rent`
  - `book_id`: char[6], Not NULL, PK
  - `title`: char[100], Not NULL
  - `series`: float(*cuz some books have 3.5), Not NULL
  - `byname1`, `byname2`: char[50]
  - `location`: char[4], Not NULL
  - `can_rent`: bool, Not NULL
- category: `book_id` | `category` | `language`
  - `book_id`: char[6], Not NULL, PK
  - `category`: char[5], Not NULL
  - `language`: char[3], Not NULL
- reader: `student_name` | `student_num`
  - `student_name`: char[5], Not NULL
  - `student_num`: char[9], Not NULL, PK
- rent: `student_num` | `book_id` | `rent_date`
  - `student_num`: char[9], Not NULL, PK
  - `book_id`: char[6], Not NULL, PK
  - `rent_date`: date
- savings: `name` | `goods` | `date`
  - `name`: char[7]
  - `goods`: char[100]
  - `date`: date
### event
- midterm202402: `student_name` | `weights`
  - `student_name`: char[10]
  - `weights`: float
