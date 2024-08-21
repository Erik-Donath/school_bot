import datetime
import aiohttp
import icalendar

# preset_what values
PW_All = "all"
PW_CATEGORIES = "categories"
PW_COURSES = "courses"
PW_USER = "user"

# preset_time values
PT_WEEKNOW = "weeknow"
PT_WEEKNEXT = "weeknext"
PT_MONTHNOW = "monthnow"
PT_RECENTUPCOMING = "recentupcoming"
PT_CUSTOM = "custom"


class CalenderEntry:
    title: str
    content: str
    categories: str
    start: datetime
    end: datetime
    last_modified: datetime

    def __init__(self, title: str, content: str, categories: str,
                 start: datetime, end: datetime, last_modified: datetime) -> None:
        self.title, self.content, self.categories = title, content, categories
        self.start, self.end, self.last_modified = start, end, last_modified

    def __str__(self) -> str:
        return (f'\"{self.title}\" in Categories: \"{self.categories}\" '
                f'from {self.start} to {self.end}; last modified: {self.last_modified}')

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash((self.title, self.content, self.categories, self.start, self.end, self.last_modified))

    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()


class MoodleAPI:
    domain: str
    userid: str
    token: str

    def __init__(self, domain: str, userid: str, token: str) -> None:
        self.domain = domain
        self.userid = userid
        self.token = token

    def url(self, what: str, time: str) -> str:
        return (
            f"https://{self.domain}/calendar/export_execute.php?"
            f"userid={self.userid}&authtoken={self.token}"
            f"&preset_what={what}&preset_time={time}"
        )

    async def fetch(self, what: str, time: str) -> None | str:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url(what, time)) as resp:
                    if resp.status != 200:
                        print(f"Failed to fetch Moodle api. Status Code: {resp.status}")
                        return None
                    result = await resp.text()
                    if result == "Invalid authentication":
                        print("Failed to fetch Moodle api. Invalid authentication.")
                        return None
                    resp.close()
                await session.close()
            return result
        except Exception as e:
            print(f"Failed to fetch Moodle api. Exception: {e}")
            return None

    async def parse_calender(self, what: str, time: str) -> list[CalenderEntry]:
        try:
            icl_raw = await self.fetch(what, time)
            icl = icalendar.Calendar.from_ical(icl_raw)
        except Exception as e:
            print(f"Failed to parse Calender. Exception: {e}")
            return []

        entries: list[CalenderEntry] = []
        for component in icl.walk():
            if component.name == "VEVENT":
                entries.append(CalenderEntry(
                    title=component.get("SUMMARY").strip(),
                    categories=component.get("CATEGORIES").to_ical().decode("utf-8").strip(),
                    content=component.get("DESCRIPTION").strip(),
                    start=component.get("DTSTART").dt,
                    end=component.get("DTEND").dt,
                    last_modified=component.get("LAST-MODIFIED").dt,
                ))
        print(f"Found {len(entries)} Calender entries.\n{entries}")
        return entries
