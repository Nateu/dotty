import datetime as date_stuff
from datetime import datetime

from expects import equal, expect
from mamba import context, describe, it

from bot.statics import ago, get_config, jid_to_username, timestamp_to_datetime


with describe("Given a jid") as self:
    with context("when it is turned into a username"):
        with it("should take the part before the @ sign minus the last 4 characters"):
            jid = "user_name_a3k@talk.kik.com"
            expect(jid_to_username("user_name_a3k@talk.kik.com")).to(equal("user_name"))

with describe("Given a set of configuration json") as self:
    with context("when you get config"):
        with it("should return the json as an object"):
            config = get_config()
            expect(config["bot"]["name"]).to(equal("Dotty bot"))

with describe("Given a timestamp") as self:
    with context("when it is converted to a datetime object"):
        with it("should a datetime object"):
            dt = timestamp_to_datetime(277894800)
            expect(str(dt)).to(equal("1978-10-22 09:00:00"))

with describe("Given a datetime object") as self:
    with context("when it is one second in the future"):
        with it("should return just now"):
            now = datetime.utcnow()
            input_value = now + date_stuff.timedelta(seconds=1)
            expect(ago(input_value)).to(equal("sometime in the future?!"))

    with context("when it was 9 seconds ago"):
        with it("should return just now"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=9)
            expect(ago(input_value)).to(equal("just now"))

    with context("when it was 10 seconds ago"):
        with it("should return 10 seconds ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=10)
            expect(ago(input_value)).to(equal("10 seconds ago"))

    with context("when it was 59 seconds ago"):
        with it("should return 59 seconds ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59)
            expect(ago(input_value)).to(equal("59 seconds ago"))

    with context("when it was 1 minute ago"):
        with it("should return a minute ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(minutes=1)
            expect(ago(input_value)).to(equal("a minute ago"))

    with context("when it was 1 minute and 59 seconds ago"):
        with it("should return a minute ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=1)
            expect(ago(input_value)).to(equal("a minute ago"))

    with context("when it was 2 minutes ago"):
        with it("should return 2 minutes ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(minutes=2)
            expect(ago(input_value)).to(equal("2 minutes ago"))

    with context("when it was 59 minutes and 59 seconds ago"):
        with it("should return 59 minutes ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=59)
            expect(ago(input_value)).to(equal("59 minutes ago"))

    with context("when it was 1 hour ago"):
        with it("should return an hour ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(hours=1)
            expect(ago(input_value)).to(equal("an hour ago"))

    with context("when it was 1 hours, 59 minutes and 59 seconds ago"):
        with it("should return an hour ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=59, hours=1)
            expect(ago(input_value)).to(equal("an hour ago"))

    with context("when it was 2 hours ago"):
        with it("should return 2 hours ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(hours=2)
            expect(ago(input_value)).to(equal("2 hours ago"))

    with context("when it was 23 hours, 59 minutes and 59 seconds ago"):
        with it("should return 23 hours ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=59, hours=23)
            expect(ago(input_value)).to(equal("23 hours ago"))

    with context("when it was 1 day ago"):
        with it("should return yesterday"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(days=1)
            expect(ago(input_value)).to(equal("yesterday"))

    with context("when it was 6 days, 23 hours, 59 minutes and 59 seconds ago"):
        with it("should return 6 days ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=59, hours=23, days=6)
            expect(ago(input_value)).to(equal("6 days ago"))

    with context("when it was 7 day ago"):
        with it("should return a week ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(days=7)
            expect(ago(input_value)).to(equal("a week ago"))

    with context("when it was 13 days, 23 hours, 59 minutes and 59 seconds ago"):
        with it("should return a week ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=59, hours=23, days=13)
            expect(ago(input_value)).to(equal("a week ago"))

    with context("when it was 55 days, 23 hours, 59 minutes and 59 seconds ago"):
        with it("should return 3 weeks ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=59, hours=23, days=55)
            expect(ago(input_value)).to(equal("7 weeks ago"))

    with context("when it was 56 days ago"):
        with it("should return a month ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(days=56)
            expect(ago(input_value)).to(equal("a month ago"))

    with context("when it was 59 days, 23 hours, 59 minutes and 59 seconds ago"):
        with it("should return a month ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(seconds=59, minutes=59, hours=23, days=59)
            expect(ago(input_value)).to(equal("a month ago"))

    with context("when it was 61 days ago"):
        with it("should return 2 months ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(days=61)
            expect(ago(input_value)).to(equal("2 months ago"))

    with context("when it was 366 days ago"):
        with it("should return a year ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(days=366)
            expect(ago(input_value)).to(equal("a year ago"))

    with context("when it was 731 days ago"):
        with it("should return 2 years ago"):
            now = datetime.utcnow()
            input_value = now - date_stuff.timedelta(days=731)
            expect(ago(input_value)).to(equal("2 years ago"))
