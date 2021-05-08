@app.route('/tour-detail/<int:id>', methods=['GET'])
@login_required
def tour_detail(id):
	tour_detail = User.query.filter_by(id=id).first()
    return render_template('tour-detail.html', tour_detail=tour_detail)
