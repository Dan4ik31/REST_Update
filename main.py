import json

from flask import Flask, request

from src.subject import Subject
from src.book import Book

api=Flask(__name__)

data: {Subject} = {}
autoincrement_subject_id = 0
autoincrement_book_id = 0

@api.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = data.get(request.headers.get('x-username'))
    if subjects is None:
        return '[]'

    result = []
    for subject in subjects:
        result_item = {}
        result_item["id"] = subject.id
        result_item["name"] = subject.name
        result_item["books"] = []
        for book in subject.book:
            result_item["books"].append({
                "id": book.id,
                "name": book.name,
            })
        result.append(result_item)

    return json.dumps(result)


@api.route('/subject/<int:subject_id>', methods=['GET'])
def get_subjects_by_id(subject_id):
    subjects = data.get(request.headers.get('x-username'))
    if subjects is None:
        return '[]'

    result = []
    for subject in subjects:
        if subject.id == subject_id:
            for book in subject.book:
                result.append({
                    "id": book.id,
                    "name": book.name,
                })

    return json.dumps(result)

@api.route('/insert', methods=['POST'])
def insert_book():
    if data.get(request.headers.get('x-username')) is None:
        data[(request.headers.get('x-username'))] = []

    subjects = data.get(request.headers.get('x-username'))
    subject_name = request.form["subject_name"]
    book_name = request.form["book_name"]
    subject_exist = None
    for subject in subjects:
        if subject.name == subject_name:
           subject_exist = subject
            break

    if subject_exist is None:
        global autoincrement_subject_id
        autoincrement_subject_id +=1
        subject_exist = Subject(autoincrement_subject_id)
        subject_exist.book = []
        subject_exist.name = subject_name
        subjects.append(subject_exist)

    global autoincrement_book_id
    autoincrement_book_id += 1
    book = Book(autoincrement_book_id, book_name)
    subject_exist.book.append(book)


@api.route('/update', methods=['PUT'])
def update_book():
    if data.get(request.headers.get('x-username')) is None:
        return

    subjects = data.get(request.headers.get('x-username'))

    subject_name = request.form["subject_name"]
    book_name = request.form["book_name"]
    new_book_name = request.form["new_book_name"]
    subject_exist = None
    for subject in subjects:
        if subject.name == subject_name:
            subject_exist = subject
            break

    if subject_exist is not None:
        for book in subject_exist.book:
            if book.name == book_name:
                book.name = new_book_name
                break

@api.route('/delete', methods=['DELETE'])
def delete_book():
    if data.get(request.headers.get('x-username')) is None:
        return

    subjects = data.get(request.headers.get('x-username'))
    subject_name = request.form["subject_name"]
    book_name = request.form["book_name"]
    subject_exist = None
    for subject in subjects:
        if subject.name == subject_name:
            subject_exist = subject
            break

    if subject_exist is not None:
        for book in subject_exist.book:
            if book.name == book_name:
                subject_exist.book.remove(book)
                break


if __name__ == '__main__':
    api.run('127.0.0.1', 8888)
