from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
from sqlalchemy import Float
import uuid  # Import the uuid module

# from application.forms import LoginForm
from application.database.user.user_db import db,Event,Guests,User,Booking,Rooms,Payment,Reservation,Refund,Budget,Income,Expenses,Attendance,Iteman,Family,Category,Unit,Stock,Store,StockTransfer,Department,Vendor,PurchaseOrder,PurchaseRequest,ReceivedItem,returnRequest,GOP,RoomType,Session,Wifi,Noticer,Employee
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session
from flask import request, jsonify, send_from_directory
import os
import base64
from datetime import datetime

guest = Blueprint("guest", __name__)




# Ensure to define your upload directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Now, define the UPLOAD_FOLDER path using the absolute path
UPLOAD_FOLDER = os.path.join(project_root, 'uploads')

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
class Guest_schema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","unit","Category","family","open_by","department","price","address","has_checkout","checkout_date","arrival","city","country","id_type","id_number","id_upload","dob","gender","work","remark","phone",
                "region","email","username","arrival_date","checkout_date","guest_id","note","amount","created_date","date","type","attendace","name","description","store","quantity","hod","requested_by","item","approved_by",
                "total_cost","unit_price","store","status","Department","attendance","time_in","time_out","position","reason","voided","item_id","request_by","user",
                    "close_by","open_date","close_date","wifi_code","role","letter","picture_one","picture_two","picture_three","picture_four","picture_five","cover_picture")


class Refund_Schema(ma.Schema):
    class Meta:
        fields=("id","reason","refund_amount","payment_id","name","refund_time","status","authorized_by","session")


        
        
class PaySchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","balance","method","children","adult","wifi_code","payment","checkin_date","checkout_date","room_type","discount","status","payment_date","guest_id","booking_id","session","code")

class ReserveSchema(ma.Schema):
    class Meta:
        fields=("id","name","price","status","room_number","room_type","payment_status","arrival","departure","payment_date",
                "adult","children","purpose","departure","room_nmber","created_date","Payment_status","country","email","phone")

refund_schema = Refund_Schema(many=True)
guest_schema = Guest_schema(many=True)

pay_schema = PaySchema(many=True)

reserve_schema =ReserveSchema(many=True)





@guest.route("/add_guest",methods=["POST"])
@flask_praetorian.auth_required

def add_guest():
        
        username= request.json["username"]
        email= request.json["email"]
        password= request.json["password"]
        hashed_password= guard.hash_password(password)
        first_name= request.json["first_name"]
        last_name= request.json["last_name"]
        country= request.json["country"]
        address= request.json["address"]
        city = request.json["city"]
        
        phone = request.json["phone"]
       
        owner =Guests(   
        username= request.json["username"],
        email= request.json["email"],
        password= request.json["password"],
       
        dob= request.json["dob"],
        country= request.json["country"],
        arrival_date = request.json["arrival_date"],
        # photo = request.json["photo"],
        # id_type = request.json["id_type"],
        # id_upload= request.json["id_upload"],



        # id_number= request.json["id_number"],
        checkout_date= request.json["checkout_date"],
        remark= request.json["remark"],
        work= request.json["work"],
        city = request.json["city"],
        gender = request.json["gender"],
        phone = request.json["phone"],
        address= request.json["address"],
        first_name= request.json["first_name"],
        last_name= request.json["last_name"],
        region= request.json["region"],


                      created_by_id =  flask_praetorian.current_user().id
      
        )
        user =User(username=username,email=email,hashed_password=hashed_password,roles="guest",
                   created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),  firstname= first_name, lastname=last_name,
        country= country,address= address,
        city = city,  phone = phone)
        db.session.add(user)
        db.session.commit()
        db.session.add(owner)
        db.session.commit()
        db.session.close()
     
  
        # db.session.close()
        resp = jsonify("success")
        resp.status_code=200
        return resp


@guest.route("/get_all_guest",methods=["GET"])
@flask_praetorian.auth_required
def get_all_guest():
    guests = Guests.query.all()
    results = guest_schema.dump(guests)

    return jsonify(results)

@guest.route("/add_expense", methods=['POST'])
@flask_praetorian.auth_required
def add_expense():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        name = request.json["name"]
        amount = request.json["amount"]
        note = request.json["note"]
        date = request.json["date"]
        usr = user.firstname + " " + user.lastname
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        exp = Expenses(name=name, amount=amount, note=note, date=date,
                       user=usr, created_by_id=flask_praetorian.current_user().id,
                       created_date=created_date)

        db.session.add(exp)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 200
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route("/get_expense_list", methods=['GET'])
@flask_praetorian.auth_required
def get_expense_list():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        exp = Expenses.query.filter_by(created_by_id=user.id).all()
        result = guest_schema.dump(exp)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_expense/<id>", methods=['GET'])
@flask_praetorian.auth_required
def get_expense(id):
    try:
        exp = Expenses.query.filter_by(id=id).first()
        if not exp:
            return jsonify({"error": "Expense not found"}), 404
        
        result = guest_schema.dump(exp)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_event/<id>", methods=['GET'])
@flask_praetorian.auth_required
def get_event(id):
    try:
        exp = Event.query.filter_by(id=id).first()
        if not exp:
            return jsonify({"error": "Event not found"}), 404

        result = guest_schema.dump(exp)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/update_expense", methods=['PUT'])
@flask_praetorian.auth_required
def update_expense():
    try:
        id = request.json["id"]
        sub_data = Expenses.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Expense not found"}), 404
        
        sub_data.name = request.json["name"]
        sub_data.amount = request.json["amount"]
        sub_data.note = request.json["note"]
        sub_data.date = request.json["date"]
        
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route("/delete_expense/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_expense(id):
    try:
        sub_data = Expenses.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Expense not found"}), 404

        db.session.delete(sub_data)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500





@guest.route("/guest_info/<id>",methods=["GET"])
@flask_praetorian.auth_required
def guest_info(id):
    guests = db.session.query(Guests).filter_by(id = id).all()
    results = guest_schema.dump(guests)

    return jsonify(results)








@guest.route("/update_guest",methods=["PUT"])
@flask_praetorian.auth_required

def update_guest():
        id = request.json["id"]
        guest = Guests.query.filter_by(id=id).first()
        guest.username= request.json["username"]
        guest.email= request.json["email"]
        password= request.json["password"]
        guest.hashed_password= guard.hash_password(password)
       
       
        guest.dob= request.json["dob"]
        guest.country= request.json["country"]
        guest.arrival_date = request.json["arrival_date"]
       


        
        guest.checkout_date= request.json["checkout_date"]
        guest.remark= request.json["remark"]
        guest.work= request.json["work"]
        guest.city = request.json["city"]
        guest.gender = request.json["gender"]
        guest.phone = request.json["phone"]
        guest.address= request.json["address"]
        guest.first_name= request.json["first_name"]
        guest.last_name= request.json["last_name"]
        guest.region= request.json["region"]


        # guest.created_by_id =  flask_praetorian.current_user().id
      

    
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code=200
        return resp



@guest.route("/delete_guest/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_guest(id):
    gst = db.session.query(Guests).filter_by(id =id).first()
    usr =  db.session.query(User).filter_by(username =gst.username).first()
    db.session.delete(gst)
    # db.session.delete(usr)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200

    return resp


@guest.route("/fetch_guest/<id>",methods=["GET"])
def fetch_guest(id):
      gst = db.session.query(Guests).filter_by(id=id).all()
      results = guest_schema.dump(gst)
      return jsonify(results)




@guest.route("/add_booking",methods=["POST"])
@flask_praetorian.auth_required
def add_booking():
    session = Session.query.filter_by(status="current").first()
    if session:
        open_date=session.open_date
    room_number=request.json["room_number"]
    name=request.json["name"]
    guest_id = request.json["guest_id"]
    booking = Booking(name=request.json["name"],  room_type=request.json["room_type"],country=request.json["country"],session=open_date,
    
     purpose=request.json["purpose"],
      
     
     departure_date=request.json["departure_date"],
     
     arrival_date =request.json["arrival_date"],
     adult =request.json["adult"],
     children=request.json["children"],



     room_number=request.json["room_number"],
     has_checkout=False,
     
     status=request.json["status"],
     create_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
     created_by_id = flask_praetorian.current_user().id,guest_id=guest_id,
    )
    room = Rooms.query.filter_by(room_number=room_number).first()
    guest = Guests.query.filter_by(id=guest_id).first()
    guest.room_number = room_number
   
    db.session.add(booking)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200
    
    return resp

@guest.route("/add_payment", methods=["POST"])
@flask_praetorian.auth_required
def add_payment():
    try:
        session = Session.query.filter_by(status="current").first()
        if session:
            open_date = session.open_date
        else:
            return jsonify({"error": "No active session found"}), 404

        amount = request.json.get("amount")
        name = request.json.get("name")
        usr = Employee.query.filter_by(member_id=name).first()
        if not usr:
            return jsonify({"error": "Employee not found"}), 404

        status = request.json.get("status")
        member_id = request.json.get("member_id")

        # Create a new payment entry
        pay = Payment(
            name=usr.first_name + ' ' + usr.last_name,
            amount=amount,
            refund_amount="0",
            balance=request.json.get("balance"),
            method=request.json.get("method"),
            room_type=request.json.get("room_type"),
            guest_id=request.json.get("member_id"),
            payment_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            status=status,
            session=open_date,
            created_by_id=flask_praetorian.current_user().id
        )

        inc = Income(
            amount=amount,
            date=datetime.now().strftime('%Y-%m-%d'),
            note=request.json.get("room_type"),
            created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            created_by_id=flask_praetorian.current_user().id
        )

        # Commit the changes to the database
        db.session.add(pay)
        db.session.add(inc)
        db.session.commit()

        # Send email
        usr = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        payment_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        email_message = f"""
        Hello Kevin,

        A new booking payment has been recorded in your Sikadwamma Management System.

        **Payment Details:**
        - Guest Name: {name}
        - Payment Amount: ${amount}
        - Fee Type: {request.json.get("room_type")}
        - Balance: ${request.json.get("balance")}
        - Payment Method: {request.json.get("method")}

        - Payment Status: Success
        - Date|Time: {payment_date}

        **Issued By:**
        - {usr.firstname} {usr.lastname}

        Please log in to review this transaction.

        Best regards,  
        **Kevo Executive Hotel Team**
        """

        # Send the email (commented out as per the original code)
        # msg = Message(
        #     subject="New Booking Payment - Kevo Executive Hotel",
        #     sender="jxkalmhefacbuk@gmail.com",
        #     recipients=["info@sikadwammaassociation.com"]
        # )
        # msg.body = email_message
        # mail.send(msg)

        return jsonify("success"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()


@guest.route("/get_payment", methods=["GET"])
@flask_praetorian.auth_required
def get_payment():
    try:
        pay = Payment.query.all()
        result = pay_schema.dump(pay)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_my_payment", methods=["GET"])
@flask_praetorian.auth_required
def get_my_payment():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        pay = Payment.query.filter_by(guest_id=user.username).all()
        result = pay_schema.dump(pay)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/current_payment", methods=["GET"])
@flask_praetorian.auth_required
def current_payment():
    try:
        current_year = datetime.now().year
        payments = Payment.query.filter(Payment.payment_date.like(f"%{current_year}%")).order_by(Payment.payment_date.desc()).all()
        result = pay_schema.dump(payments)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/add_notice", methods=['POST'])
@flask_praetorian.auth_required
def add_notice():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        name = request.json["name"]
        note = request.json["note"]
        date = request.json["date"]

        try:
            letter = request.json["letter"]
        except KeyError:
            letter = ""

        role = request.json.get("role", "")
        rle = ""

        if role == "all":
            rle = "Member, President, Treasurer, Secretary, Vice President, Organizer, Financial Secretary, Deputy Organizer"
        else:
            rle = role

        created_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        if letter:
            try:
                if letter.startswith("data:application/pdf;base64,"):
                    letter = letter.split(',')[1]
                letter_data = base64.b64decode(letter)
                unique_filename = str(uuid.uuid4()) + ".pdf"
                file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                with open(file_path, "wb") as f:
                    f.write(letter_data)
                letter = unique_filename
            except Exception as e:
                return jsonify({"error": f"Failed to process the PDF: {str(e)}"}), 400

        ntc = Noticer(
            name=name,
            note=note,
            date=date,
            created_by_id=flask_praetorian.current_user().id,
            letter=letter,
            created_date=created_date,
            role=rle
        )

        db.session.add(ntc)
        db.session.commit()
        db.session.close()

        return jsonify("success"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route('/download/<filename>', methods=['GET'])
def download_pdf(filename):
    print(f"Requested filename: {filename}")  # Debugging line
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@guest.route("/get_notice_list", methods=['GET'])
@flask_praetorian.auth_required
def get_notice_list():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        if user.roles == "sAdmin":
            return jsonify({"status": "success"}), 200
        ntc = Noticer.query.filter(Noticer.role.contains(user.roles)).order_by(desc(Noticer.date))
        result = guest_schema.dump(ntc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_all_notice_list", methods=['GET'])
@flask_praetorian.auth_required
def get_all_notice_list():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        ntc = Noticer.query.order_by(desc(Noticer.date))
        result = guest_schema.dump(ntc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_notice/<id>", methods=['GET'])
@flask_praetorian.auth_required
def get_notice(id):
    try:
        ntc = Noticer.query.filter_by(id=id).first()
        if not ntc:
            return jsonify({"error": "Notice not found"}), 404
        result = guest_schema.dump(ntc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/update_notice", methods=['PUT'])
@flask_praetorian.auth_required
def update_notice():
    try:
        id = request.json["id"]
        sub_data = Noticer.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Notice not found"}), 404

        role = request.json.get("role", "")
        rle = ""

        if role == "all":
            rle = "Member, President, Treasurer, Secretary, Vice President, Organizer, Financial Secretary, Deputy Organizer"
        else:
            rle = role

        letter = request.json.get("letter", sub_data.letter)

        sub_data.name = request.json["name"]
        sub_data.role = rle
        sub_data.note = request.json["note"]
        sub_data.date = request.json["date"]
        sub_data.letter = letter

        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route("/delete_notice/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_notice(id):
    try:
        sub_data = Noticer.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Notice not found"}), 404

        db.session.delete(sub_data)
        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
@guest.route("/get_return_request", methods=["GET"])
@flask_praetorian.auth_required
def get_return_request():
    """
    Retrieve all return requests ordered by their creation date.
    """
    refund = returnRequest.query.order_by(returnRequest.created_date)
    result = guest_schema.dump(refund)
    return jsonify(result)


@guest.route("/search_refund_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates():
    """
    Search for refund records by the session date.
    Filters the refund records by the provided 'date'.
    """
    date = request.json["date"]
    print(date)
    refund = Refund.query.filter(Refund.session.contains(date))
    lst = refund.order_by(desc(Refund.session))
    result = refund_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_return_date", methods=["POST"])
@flask_praetorian.auth_required
def search_return_date():
    """
    Search for return requests by the created date and status.
    Filters return requests based on the 'Success' status and the given 'date'.
    """
    date = request.json["date"]
    print(date)
    refund = returnRequest.query.filter(
        returnRequest.created_date.contains(date), returnRequest.status.contains("Success")
    )
    lst = refund.order_by(desc(returnRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_purchase_date", methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date():
    """
    Search for purchase requests based on the created date.
    Filters purchase requests by the given 'date'.
    """
    date = request.json["date"]
    print(date)
    refund = PurchaseRequest.query.filter(PurchaseRequest.created_date.contains(date))
    lst = refund.order_by(desc(PurchaseRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_order_date", methods=["POST"])
@flask_praetorian.auth_required
def search_order_date():
    """
    Search for purchase orders based on the created date.
    Filters purchase orders by the given 'date'.
    """
    date = request.json["date"]
    print(date)
    refund = PurchaseOrder.query.filter(PurchaseOrder.created_date.contains(date))
    lst = refund.order_by(desc(PurchaseOrder.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_received_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_received_dates():
    """
    Search for received items based on the created date.
    Filters received items by the given 'date'.
    """
    date = request.json["date"]
    refund = ReceivedItem.query.filter(ReceivedItem.created_date.contains(date))
    lst = refund.order_by(desc(ReceivedItem.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_stock_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_stock_dates():
    """
    Search for stock records based on the created date.
    Filters stock records by the given 'date'.
    """
    date = request.json["date"]
    refund = Stock.query.filter(Stock.created_date.contains(date))
    lst = refund.order_by(desc(Stock.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/searchdates", methods=["POST"])
@flask_praetorian.auth_required
def searchdates():
    """
    Search for payment records based on the session date.
    Filters payments by the provided 'date'.
    """
    date = request.json["date"]
    pay = Payment.query.filter(Payment.session.contains(date))
    lst = pay.order_by(desc(Payment.session))
    result = pay_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_payment_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date_two():
    """
    Search for payment records based on two session dates.
    Filters payments that match either 'date' or 'date_two' and have a balance > 0.
    """
    date = request.json.get("date")
    date_two = request.json.get("date_two")
    
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    payments = Payment.query.filter(
        or_(
            Payment.session.contains(date),
            Payment.session.contains(date_two)
        )
    ).filter(
        Payment.balance.cast(Float) > 0
    ).filter(
        Payment.session != None
    ).order_by(Payment.session.desc())

    result = pay_schema.dump(payments)
    return jsonify(result)


@guest.route("/search_payment_date", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date():
    """
    Search for payment records based on a specific session date.
    Filters payments by the provided 'date' and ensures the balance is greater than 0.
    """
    date = request.json.get("date")
    date_two = request.json.get("date_two")
    
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    payments = Payment.query.filter(
        Payment.session.contains(date),
        Payment.balance.cast(Float) > 0
    ).order_by(Payment.session.desc())

    result = pay_schema.dump(payments)
    return jsonify(result)


@guest.route("/get_payment_for/<id>", methods=["GET"])
@flask_praetorian.auth_required
def get_payment_for(id):
    """
    Retrieve a specific payment record by its ID.
    """
    pay = Payment.query.filter_by(id=id).all()
    result = pay_schema.dump(pay)
    return jsonify(result)


@guest.route("/filter_payment_day/<day>", methods=["GET"])
@flask_praetorian.auth_required
def filter_payment_day(day):
    """
    Filter payments based on the selected day type ('daily').
    Retrieves payments based on the current day's payments.
    """
    result = "yes"
    if day == "daily":
        pay = Payment.query.filter(Payment.payment_day <= datetime.now()).all()
        result = pay_schema.dump(pay)
    return jsonify(result)




@guest.route("/update_payment", methods=["PUT"])
@flask_praetorian.auth_required
def update_payment():
    try:
        amount = request.json["amount"]
        id = request.json["id"]
        
        # Query the payment by ID
        pay = Payment.query.filter_by(id=id).first()

        # Update the amount by adding the new amount to the existing amount
        a = pay.amount = int(amount) + int(pay.amount)
        pay.amount = a
        pay.method = request.json["method"]
        pay.room_type = request.json["room_type"]
        pay.discount = request.json["discount"]
        pay.children = request.json["children"]
        pay.adult = request.json["adult"]
        pay.checkin_date = request.json["checkin_date"]
        pay.checkout_date = request.json["checkout_date"]
        pay.status = request.json["status"]
        pay.balance = a
        
        # Commit the changes to the database
        db.session.commit()

        # Re-query the payment to get the most recent data
        p = Payment.query.filter_by(id=id).first()

        # Calculate the new balance
        b = int(p.amount) - int(p.balance)
        p.balance = b
        db.session.commit()

        resp = jsonify("success")
        resp.status_code = 200
        return resp
    
    except Exception as e:
        db.session.rollback()  # Rollback the session in case of any error
        print(f"Error in update_payment: {e}")
        return jsonify({"error": "Failed to update payment"}), 500


@guest.route("/update_payment_checkout", methods=["PUT"])
@flask_praetorian.auth_required
def update_payment_checkout():
    try:
        amount = request.json["amount"]
        id = request.json["id"]
        
        # Query the payment by ID
        pay = Payment.query.filter_by(id=id).first()
        guest_id = request.json["guest_id"]
        
        # Update the amount by adding the new amount to the existing amount
        a = pay.amount = int(amount) + int(pay.amount)
        pay.amount = a
        pay.method = request.json["method"]
        pay.room_type = request.json["room_type"]
        pay.discount = request.json["discount"]
        pay.children = request.json["children"]
        pay.adult = request.json["adult"]
        pay.checkin_date = request.json["checkin_date"]
        pay.checkout_date = request.json["checkout_date"]
        pay.status = request.json["status"]
        pay.balance = a
        
        # Commit the changes to the database
        db.session.commit()

        # Re-query the payment to get the most recent data
        p = Payment.query.filter_by(id=id).first()

        # Calculate the new balance
        b = int(p.amount) - int(p.balance)
        p.balance = b
        book = Booking.query.filter_by(guest_id=p.guest_id).first()
        guest = Guests.query.filter_by(id=book.guest_id).first()
        room = Rooms.query.filter_by(room_number=book.room_number).first()

        # Commit the balance update
        db.session.commit()

        payments = Payment.query.filter_by(guest_id=guest_id, status="success").all()
        if not payments:
            return jsonify({"error": "No successful payments found for this guest"}), 404
        
        total_balance = sum(float(payment.balance) for payment in payments if payment.balance and payment.balance.replace('.', '', 1).isdigit())
        if total_balance <= 0:
            book.has_checkout = True
            room.occupied_by = "none"
            room.occupied_state = "available"
            guest.has_checkout = datetime.now().strftime('%Y-%m-%d %H:%M')
            db.session.commit()

        else:
            return 401
        
        resp = jsonify("success")
        resp.status_code = 200
        return resp

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of any error
        print(f"Error in update_payment_checkout: {e}")
        return jsonify({"error": "Failed to update payment during checkout"}), 500


@guest.route("/delete_payment/<id>", methods=["DELETE"])
def delete_payment(id):
    try:
        pay = Payment.query.filter_by(id=id).first()
        if not pay:
            return jsonify({"error": "Payment not found"}), 404
        
        db.session.delete(pay)
        db.session.commit()
        
        resp = jsonify("success")
        resp.status_code = 200
        return resp

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of any error
        print(f"Error in delete_payment: {e}")
        return jsonify({"error": "Failed to delete payment"}), 500


@guest.route("/checkout/<id>", methods=["PUT"])
@flask_praetorian.auth_required
def checkout(id):
    try:
        # Retrieve the booking and corresponding guest
        booking = Booking.query.filter_by(id=id).first()
        if not booking:
            return jsonify({"error": "Booking not found"}), 404

        guest = Guests.query.filter_by(id=booking.guest_id).first()
        if not guest:
            return jsonify({"error": "Guest not found"}), 404

        # Calculate the total payment balance for the guest
        payments = Payment.query.filter_by(guest_id=booking.guest_id, status="success").all()
        if not payments:
            return jsonify({"error": "No successful payments found for this guest"}), 404

        total_balance = sum(float(payment.balance) for payment in payments if payment.balance and payment.balance.replace('.', '', 1).isdigit())

        # Get the room details for checkout logic
        room = Rooms.query.filter_by(room_number=booking.room_number).first()
        if not room:
            return jsonify({"error": "Room not found"}), 404

        room_type = RoomType.query.filter_by(room_type=room.room_type).first()
        if not room_type:
            return jsonify({"error": "Room type not found"}), 404

        # Get current time for checkout logic
        current_time = datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M')

        # Check if the current date is past the departure date
        departure_date = datetime.strptime(booking.departure_date, "%Y-%m-%d")
        
        # Case: Checkout after the departure date, charge for extra days
        if current_time > departure_date:
            # Calculate the extra days the guest stayed beyond the departure date
            extra_days = (current_time - departure_date).days
            
            # Apply charges for extra days
            extra_charge_per_day = 1.0 * float(room_type.base_price)  # Modify as per your pricing rules
            extra_charge = extra_days * extra_charge_per_day
            
            total_balance += extra_charge  # Add extra charge for extra days stayed

        # Update the payment balance (whether for late checkout or not)
        last_payment = payments[-1]  # Assuming the last successful payment is the one to update
        last_payment.balance = str(total_balance)  # Convert total_balance back to string for storage

        db.session.commit()  # Commit the updated payment balance

        # Update room state and guest checkout timestamp
        room.occupied_by = "none"
        room.occupied_state = "available"
        guest.has_checkout = current_time_str
        booking.has_checkout = True

        db.session.commit()  # Commit the room and guest updates
        
        return jsonify({"message": "Checkout successful", "balance": total_balance}), 200

    except Exception as e:
        db.session.rollback()  # Rollback the session in case of any error
        print(f"Error in checkout: {e}")
        return jsonify({"error": "Failed to process checkout"}), 500

      
@guest.route("/get_refund", methods=["GET"])
@flask_praetorian.auth_required
def get_refund():
    try:
        # Query the Refund table, ordering by the latest refund time
        refund_list = Refund.query.order_by(Refund.refund_time.desc()).all()

        # Serialize the results
        result = refund_schema.dump(refund_list)

        # Return the JSON response
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/update_refund", methods=["PUT"])
@flask_praetorian.auth_required
def update_refund():
    try:
        # Get the refund ID from the request
        refund_id = request.json.get("id")

        if not refund_id:
            return jsonify({"error": "Refund ID is required"}), 400

        # Update refund status
        refund = Refund.query.filter_by(id=refund_id).first()

        if not refund:
            return jsonify({"error": "Refund not found"}), 404

        refund.status = "success"

        # Adjust payment data
        payment = Payment.query.filter_by(id=refund.payment_id).first()
        if not payment:
            return jsonify({"error": "Payment record not found"}), 404

        # Ensure refund doesn't exceed payment amount
        if int(refund.refund_amount) > int(payment.amount):
            return jsonify({"error": "Refund amount cannot exceed payment amount"}), 400

        # Update the payment amount and balance
        payment.amount = int(payment.amount) - int(refund.refund_amount)
        payment.balance = int(payment.balance) - int(refund.refund_amount)

        # Commit changes to the database
        db.session.commit()
        db.session.refresh(refund)  # Refresh the refund instance to ensure it's still valid in session
        db.session.refresh(payment)  # Refresh the payment instance as well

        # Create a beautiful email message
        email_message = f"""
        Hello,

        We are pleased to inform you that your refund request with ID **{refund_id}** has been successfully approved.

        **Refund Details:**
        - Refund ID: {refund_id}
        - Refund Amount: {refund.refund_amount}
        - Remaining Balance: {payment.balance}

        Thank you for choosing Kevo Executive Hotel. If you have any further inquiries, feel free to reach out to us.

        Best regards,  
        **Kevo Executive Hotel Team**
        """

        # Send the email
        msg = Message(
            subject="Refund Approved - Kevo Executive Hotel",
            sender="jxkalmhefacbuk@gmail.com",
            recipients=["kevinfiadzeawu@gmail.com"]
        )
        msg.body = email_message
        mail.send(msg)

        # Return success response
        return jsonify({"message": "Refund successfully approved"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()


@guest.route("/get_budget/<id>", methods=['GET'])
@flask_praetorian.auth_required
def get_budget(id):
    try:
        inc = Budget.query.filter_by(id=id).first()
        if not inc:
            return jsonify({"error": "Budget not found"}), 404
        result = guest_schema.dump(inc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/update_Budget", methods=['PUT'])
@flask_praetorian.auth_required
def update_Budget():
    try:
        id = request.json["id"]
        sub_data = Budget.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Budget not found"}), 404
        
        sub_data.name = request.json["name"]
        sub_data.amount = request.json["amount"]
        sub_data.note = request.json["note"]
        sub_data.type = request.json["type"]

        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route("/delete_budget/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_budget(id):
    try:
        sub_data = Budget.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Budget not found"}), 404
        
        db.session.delete(sub_data)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route("/add_income", methods=['POST'])
@flask_praetorian.auth_required
def add_income():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        name = request.json["name"]
        amount = request.json["amount"]
        note = request.json["note"]
        date = request.json["date"]
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        inc = Income(
            name=name,
            amount=amount,
            note=note,
            date=date,
            created_by_id=flask_praetorian.current_user().id,
            created_date=created_date
        )

        db.session.add(inc)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 200
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route("/get_income_list", methods=['GET'])
@flask_praetorian.auth_required
def get_income_list():
    try:
        inc = Income.query.all()
        result = guest_schema.dump(inc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_income/<id>", methods=['GET'])
@flask_praetorian.auth_required
def get_income(id):
    try:
        inc = Income.query.filter_by(id=id).first()
        if not inc:
            return jsonify({"error": "Income not found"}), 404
        result = guest_schema.dump(inc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/update_income", methods=['PUT'])
@flask_praetorian.auth_required
def update_income():
    try:
        id = request.json["id"]
        sub_data = Income.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Income not found"}), 404

        sub_data.name = request.json["name"]
        sub_data.amount = request.json["amount"]
        sub_data.note = request.json["note"]
        sub_data.date = request.json["date"]

        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@guest.route("/delete_income/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_income(id):
    try:
        sub_data = Income.query.filter_by(id=id).first()
        if not sub_data:
            return jsonify({"error": "Income not found"}), 404

        db.session.delete(sub_data)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code = 201
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Follow the same approach for all other routes as needed.
@guest.route("/add_budget", methods=['POST'])
@flask_praetorian.auth_required
def add_budget():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        name = request.json["name"]
        amount = request.json["amount"]
        note = request.json["note"]
        type = request.json["type"]
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        inc = Budget(name=name, amount=amount, note=note, type=type,
                     created_by_id=flask_praetorian.current_user().id,
                     created_date=created_date)

        db.session.add(inc)
        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 200
        return resp
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()


@guest.route("/get_budget_list", methods=['GET'])
@flask_praetorian.auth_required
def get_budget_list():
    try:
        inc = Budget.query.all()
        result = guest_schema.dump(inc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/search_attendance_date", methods=["POST"])
@flask_praetorian.auth_required
def search_attendance_date():
    try:
        date = request.json["date"]
        pay = Attendance.query.filter(Attendance.created_date.contains(date))
        lst = pay.order_by(desc(Attendance.created_date))
        result = guest_schema.dump(lst)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/search_income_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates():
    try:
        date = request.json.get("date")

        if not date:
            return jsonify({"error": "Date is required"}), 400

        income_records = Income.query.filter(Income.date.contains(date))
        ordered_records = income_records.order_by(desc(Income.date))
        result = guest_schema.dump(ordered_records)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/search_budget_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_budget_dates():
    try:
        date = request.json["date"]
        pay = Budget.query.filter(Budget.created_date.contains(date))
        lst = pay.order_by(desc(Budget.created_date))
        result = guest_schema.dump(lst)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/search_income_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates_two():
    try:
        date = request.json.get("date")
        date_two = request.json.get("datetwo")

        pay = Income.query.filter(
            or_(
                Income.date.contains(date),
                Income.date.contains(date_two)
            )
        ).order_by(desc(Income.date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500


@guest.route("/searchdates_two", methods=["POST"])
@flask_praetorian.auth_required
def searchdates_two():
    try:
        date = request.json.get("date")
        date_two = request.json.get("date_two")

        pay = Payment.query.filter(
            or_(
                Payment.session.contains(date),
                Payment.session.contains(date_two)
            )
        ).order_by(desc(Payment.session)).all()

        result = pay_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500


@guest.route("/search_purchase_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date_two():
    try:
        date = request.json.get("date")
        date_two = request.json.get("date_two")

        pay = PurchaseOrder.query.filter(
            or_(
                PurchaseOrder.created_date.contains(date),
                PurchaseOrder.created_date.contains(date_two)
            )
        ).order_by(desc(PurchaseOrder.created_date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500


@guest.route("/search_refund_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates_two():
    try:
        date = request.json.get("date")
        date_two = request.json.get("date_two")

        pay = Refund.query.filter(
            or_(
                Refund.session.contains(date),
                Refund.session.contains(date_two)
            )
        ).order_by(desc(Refund.refund_time)).all()

        result = refund_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500


@guest.route("/search_expense_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_dates():
    try:
        date = request.json.get("date")

        if not date:
            return jsonify({"error": "Date is required"}), 400

        expense_records = Expenses.query.filter(Expenses.date.contains(date))
        ordered_records = expense_records.order_by(desc(Expenses.date))
        result = guest_schema.dump(ordered_records)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/search_gop_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_gop_dates():
    try:
        date = request.json.get("date")

        if not date:
            return jsonify({"error": "Date is required"}), 400

        gop_records = GOP.query.filter(Expenses.date.contains(date))
        ordered_records = gop_records.order_by(desc(Expenses.date))
        result = guest_schema.dump(ordered_records)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@guest.route("/search_expense_budget_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_budget_dates():
    try:
        date = request.json.get("date")
        if not date:
            return jsonify({"error": "Date is required"}), 400
        
        pay = Budget.query.filter(Budget.term.date(date))
        lst = pay.order_by(desc(Budget.created_date))
        result = guest_schema.dump(lst)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/search_income_budget_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_income_budget_dates():
    try:
        date = request.json.get("date")
        if not date:
            return jsonify({"error": "Date is required"}), 400
        
        pay = Budget.query.filter(Budget.date.contains(date))
        lst = pay.order_by(desc(Budget.created_date))
        result = guest_schema.dump(lst)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/search_expense_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_dates_two():
    try:
        date = request.json.get("date")
        date_two = request.json.get("datetwo")
        if not date or not date_two:
            return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400
        
        pay = Expenses.query.filter(
            or_(
                Expenses.date.contains(date),
                Expenses.date.contains(date_two)
            )
        ).order_by(desc(Expenses.date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/add_store", methods=['POST'])
@flask_praetorian.auth_required
def add_store():
    try:
        name = request.json["name"]
        description = request.json["description"]
        category = request.json["category"]
        
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        inc = Store(name=name, description=description, Category=category, created_date=created_date)
  
        db.session.add(inc)
        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 200
        return resp

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_store_list", methods=['GET'])
@flask_praetorian.auth_required
def get_store_list():
    try:
        inc = Store.query.all()
        result = guest_schema.dump(inc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/update_store", methods=['PUT'])
@flask_praetorian.auth_required
def update_store():
    try:
        id = request.json["id"]
        sub_data = Store.query.filter_by(id=id).first()
        
        if not sub_data:
            return jsonify({"error": "Store not found"}), 404
        
        sub_data.name = request.json["name"]
        sub_data.description = request.json["description"]
        sub_data.Category = request.json["category"]

        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 201
        return resp

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/delete_store/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_store(id):
    try:
        sub_data = Store.query.filter_by(id=id).first()
        
        if not sub_data:
            return jsonify({"error": "Store not found"}), 404

        db.session.delete(sub_data)
        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 200
        return resp

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/add_stock", methods=['POST'])
@flask_praetorian.auth_required
def add_stock():
    try:
        name = request.json["name"]
        store = request.json["store"]
        quantity = request.json["quantity"]
        
        created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
        st = Stock.query.filter_by(name=name).first()

        if st:
            st.quantity = int(st.quantity) + int(quantity)
        else:
            inc = Stock(name=name, store=store, quantity=quantity, created_date=created_date)
            db.session.add(inc)
        
        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 200
        return resp

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/get_stock_list", methods=['GET'])
@flask_praetorian.auth_required
def get_stock_list():
    try:
        inc = Stock.query.all()
        result = guest_schema.dump(inc)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/update_stock", methods=['PUT'])
@flask_praetorian.auth_required
def update_stock():
    try:
        id = request.json["id"]
        quantity = request.json["quantity"]
        sub_data = Stock.query.filter_by(id=id).first()
        
        if not sub_data:
            return jsonify({"error": "Stock not found"}), 404

        sub_data.name = request.json["name"]
        sub_data.store = request.json["store"]
        sub_data.quantity = int(quantity) + int(sub_data.quantity)

        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 201
        return resp

    except KeyError as e:
        return jsonify({"error": f"Missing field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@guest.route("/delete_stock/<id>", methods=['DELETE'])
@flask_praetorian.auth_required
def delete_stock(id):
    try:
        sub_data = Stock.query.filter_by(id=id).first()
        
        if not sub_data:
            return jsonify({"error": "Stock not found"}), 404

        db.session.delete(sub_data)
        db.session.commit()
        db.session.close()

        resp = jsonify("success")
        resp.status_code = 200
        return resp

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Similar updates can be made to other routes based on the pattern shown above.








@guest.route("/add_department",methods=['POST'])
@flask_praetorian.auth_required
def add_department():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name = request.json["name"]
    description = request.json["description"]
    hod = request.json["hod"]
    # created_date = db.Column(db.String(400))
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Department(name=name,description=description,hod=hod,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_department_list",methods=['GET'])
@flask_praetorian.auth_required
def get_department_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Department.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_department",methods=['PUT'])
@flask_praetorian.auth_required
def update_department():
    id = request.json["id"]
    sub_data = Department.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    sub_data.Category =request.json["hod"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_department/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_department(id):
      sub_data = Department.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp




















@guest.route("/add_received_item",methods=['POST'])
@flask_praetorian.auth_required
def add_received_item():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    # store =request.json["store"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    # st = Stock.query.filter_by(name=name).first()
    # if st:
    #     st.quantity= int(st.quantity) + int(quantity)

    itm = ReceivedItem(name=name,quantity=quantity,
                   created_date=created_date)
  
    db.session.add(itm)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_received",methods=['GET'])
@flask_praetorian.auth_required
def get_received():    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    itm = ReceivedItem.query.all()
    result = guest_schema.dump(itm)
    return jsonify(result)




@guest.route("/update_received_item",methods=['PUT'])
@flask_praetorian.auth_required
def update_received_item():

    id = request.json["id"]
   
    sub_data = ReceivedItem.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.quantity= request.json["store"]
    # sub_data.store= int(quantity) + int(sub_data.quantity) 
    # sub_data.Category =request.json["category"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_received_item/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_received_item(id):
      sub_data = ReceivedItem.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp


@guest.route("/add_return_request",methods=['POST'])
@flask_praetorian.auth_required
def add_return_request():
    item_id = request.json["id"]
    item = request.json["item"]
    qty = request.json["quantity"]
    reason = request.json["reason"]
    # itm = Iteman.query.filter_by(id=id).first()
    # itm.voided="yes"
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    request_by= user.firstname +" "+ user.lastname

    a = returnRequest(item_id=item_id,item=item,quantity=qty,reason=reason,created_date=created_date,request_by=request_by,status="Pending")
    db.session.add(a)
    db.session.commit()
    resp = jsonify("success")
    resp.status_code =200
    return resp








@guest.route("/add_gop",methods=['POST'])
@flask_praetorian.auth_required
def add_gop():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    gop = GOP(name=name,amount=amount,note=note,date=date,
                   user=usr,created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date)
  
    db.session.add(gop)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_gop_list",methods=['GET'])
@flask_praetorian.auth_required
def get_gop_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    gop = GOP.query.filter_by(created_by_id=user.id)
    result = guest_schema.dump(gop)
    return jsonify(result)



@guest.route("/get_gop/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_gop(id):

    gop = GOP.query.filter_by(id=id)
    result = guest_schema.dump(gop)
    return jsonify(result)




@guest.route("/update_gop",methods=['PUT'])
@flask_praetorian.auth_required
def update_gop():
    id = request.json["id"]
    sub_data = GOP.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_gop/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_gop(id):
      sub_data = GOP.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp





@guest.route("/add_session", methods=['POST'])
@flask_praetorian.auth_required
def add_session():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    session_data = Session.query.filter_by(status="current").first()
    
    if session_data:  # Fix: Using `session_data` instead of `session`
        session_data.status = "old"
    
    usr = f"{user.firstname} {user.lastname}"
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Fix: Assign `None` instead of an empty string for close_date
    new_session = Session(
        open_date=created_date,
        close_date=None,  # Use `None` instead of `""`
       
        open_by=usr,
        status="current"
    )

    db.session.add(new_session)
    db.session.commit()
    db.session.close()

    return jsonify("success"), 200



@guest.route("/close_session",methods=['PUT'])
@flask_praetorian.auth_required
def close_session():
    id = request.json["id"]
   

    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
  
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    session_data = Session.query.filter_by(id=id).first()
    session_data.status="old"
    session_data.close_by=usr
    session_data.close_date=created_date
  
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp


@guest.route("/get_current_session")
@flask_praetorian.auth_required
def get_current_session():
    session_data =  Session.query.filter_by(status="current").all()
    results = guest_schema.dump(session_data)
    return jsonify(results)



@guest.route("/get_all_session")
@flask_praetorian.auth_required
def get_all_session():
    session_data =  Session.query.order_by(desc(Session.open_date))
    results = guest_schema.dump(session_data)
    return jsonify(results)


@guest.route("/get_wifi_code", methods=["POST"])
@flask_praetorian.auth_required
def get_wifi_code():
    data = request.json  # Get full JSON data
    print("Received data:", data)  # Debugging log
    days = data.get("days")  # Use .get() to avoid KeyError
    
    if not days:
        return jsonify({"error": "Missing 'days' in request"}), 400  # Return error if days is missing

    print("Days:", days)  # Confirm 'days' value is received

    # Query for an available WiFi code
    wifi_code = Wifi.query.filter_by(state="available", duration=days).order_by(func.random()).first()

    if not wifi_code:
        return jsonify({"error": "No available WiFi codes"}), 404  # Return 404 if no matching code is found

    results = pay_schema.dump(wifi_code, many=False) 
     # Serialize result
    print(wifi_code.code)
    print("WiFi Code Found:", results)  # Debugging log
    
    return jsonify(results)












@guest.route("/add_event",methods=['POST'])
@flask_praetorian.auth_required
def add_event():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    cover_picture =request.json["cover_picture"]
    picture_two =request.json["picture_two"]
    picture_one=request.json["picture_one"]
    picture_three =request.json["picture_three"]
    picture_four=request.json["picture_four"]
    picture_five=request.json["picture_five"]
    note= request.json["note"]
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Event(name=name,cover_picture=cover_picture,note=note,date=date,picture_four=picture_four,picture_five=picture_five,
                 picture_one=picture_one,picture_three=picture_three,picture_two=picture_two,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_event_list",methods=['GET'])
@flask_praetorian.auth_required
def get_event_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Event.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/delete_event/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_event(id):
      sub_data = Event.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp