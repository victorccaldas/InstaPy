""" Module which handles the follow features """
# import built-in & third-party modules
from random import randint
from time import sleep

# import exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# import InstaPy modules
from .util import (
    explicit_wait,
    get_username_from_id,
    is_page_available,
    load_user_id,
    update_activity,
    web_address_navigator,
)
from .xpath import read_xpath


def get_following_status(
    browser, track, username, person, person_id, logger, logfolder
):
    """Verify if you are following the user in the loaded page"""
    follow_button_error = 0 
    while True:
        if person == username:
            return "OWNER", None

        if track == "profile":
            ig_homepage = "https://www.instagram.com/"
            web_address_navigator(browser, ig_homepage + person)

        follow_button_XP = read_xpath(get_following_status.__name__, "follow_button_XP")
        failure_msg = "--> Unable to detect the following status of '{}'!"
        user_inaccessible_msg = (
            "Couldn't access the profile page of '{}'!\t~might have changed the"
            " username".format(person)
        )

        # check if the page is available
        valid_page = is_page_available(browser, logger)
        
        if not valid_page:
            logger.warning(user_inaccessible_msg)
            person_new = verify_username_by_id(
                browser, username, person, None, logger, logfolder
            )
            if person_new:
                ig_homepage = "https://www.instagram.com/"
                web_address_navigator(browser, ig_homepage + person_new)
                valid_page = is_page_available(browser, logger)
                
                if not valid_page:
                    logger.error(failure_msg.format(person_new.encode("utf-8")))
                    return "UNAVAILABLE", None
            else:
                logger.error(failure_msg.format(person.encode("utf-8")))
                return "UNAVAILABLE", None

        # wait until the follow button is located and visible, then get it
        # Deixar verificação do follow button por ultimo: devido à presença de follow buttons
        # quando existe a janelinha do Suggestions for You
        try:
            follow_button = browser.find_element(
                By.XPATH,
                read_xpath(get_following_status.__name__, "follow_span_XP_following"),
            )
            return "Following", follow_button
        except NoSuchElementException:
            try:
                follow_button_XP = read_xpath(get_following_status.__name__, "follow_button_XP")
                browser.find_element(By.XPATH, follow_button_XP)

            except NoSuchElementException:
                return "UNAVAILABLE", None

        follow_button = explicit_wait(
            browser, "VOEL", [follow_button_XP, "XPath"], logger, 7, False
        )

        if not follow_button:
            browser.execute_script("location.reload()")
            update_activity(browser, state=None)
            sleep(randint(5, 10))

            follow_button = explicit_wait(
                browser, "VOEL", [follow_button_XP, "XPath"], logger, 14, False
            )
            if not follow_button:
                # cannot find the any of the expected buttons
                logger.error(failure_msg.format(person.encode("utf-8")))
                return None, None

        # get follow status
        try:
            following_status = follow_button.text
            break
        except Exception as e:
            # tentar novamente
            follow_button_error += 1
            if follow_button_error > 3:
                print("follow_button_error 3x seguidas: Permitindo o erro acontecer..")
                raise e
    if follow_button_error > 0:
        logger.info("Erro corrigido :) precisou de {} tentativas.".format(follow_button_error+1))
    return following_status, follow_button


def verify_username_by_id(browser, username, person, person_id, logger, logfolder):
    """Check if the given user has changed username after the time of
    followed"""

    # try to find the user by ID
    person_id = load_user_id(username, person, logger, logfolder)

    # if person_id is None, inform the InstaPy user that record does not exist
    if person_id not in [None, "unknown", "undefined"]:
        # get the [new] username of the user from the stored user ID
        person_new = get_username_from_id(browser, person_id, logger)

        # if person_new is None, inform the InstaPy user that record does not exist
        if person_new is not None and person_new != person:
            logger.info(
                "User '{}' has changed username and now is called '{}' :S".format(
                    person, person_new
                )
            )
            return person_new

    # check who call this def, since will receive a None value
    logger.info("User '{}' doesn't exist in local records".format(person))
    return None
