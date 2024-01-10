
print(last_page)

comments = []

while last_page > 0:
    print(last_page)
    more_link = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.ulBlueLinks')))
    more_link[0].click()

    comment_tags = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'p.partial_entry')))
    print(comment_tags[0].text)